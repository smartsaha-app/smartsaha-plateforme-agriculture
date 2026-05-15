from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from apps.catalogue.models import Category, Product, ProductImage
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'parent', 'order']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']

class ProductSerializer(serializers.ModelSerializer):
    seller_details = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fallback pour image_url si nul mais qu'il y a des images
        if not representation.get('image_url') and instance.images.exists():
            first_image = instance.images.first()
            request = self.context.get('request')
            if request:
                representation['image_url'] = request.build_absolute_uri(first_image.image.url)
            else:
                representation['image_url'] = first_image.image.url
        return representation

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'stock', 'unit', 'source_type', 
            'seller', 'seller_details', 'image_url', 'category', 'category_name',
            'description', 'images', 'uploaded_images', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'seller', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_seller_details(self, obj):
        if not obj.seller:
            return None
        return {
            'username': obj.seller.username,
            'email': obj.seller.email,
            'first_name': obj.seller.first_name,
            'last_name': obj.seller.last_name,
        }

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        
        request = self.context.get('request')
        for index, image in enumerate(uploaded_images):
            is_main = (index == 0)
            pi = ProductImage.objects.create(product=product, image=image, is_main=is_main)
            
            # Si aucune URL n'est définie manuellement, on prend la première image uploadée
            if is_main and not product.image_url:
                if request:
                    product.image_url = request.build_absolute_uri(pi.image.url)
                else:
                    product.image_url = pi.image.url
                product.save()
        
        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if uploaded_images:
            request = self.context.get('request')
            # Si l'instance n'a pas d'image principale, on marquera la première nouvelle comme principale
            has_main = instance.images.filter(is_main=True).exists()
            
            for index, image in enumerate(uploaded_images):
                is_main = not has_main and (index == 0)
                pi = ProductImage.objects.create(product=instance, image=image, is_main=is_main)
                
                if (is_main or not instance.image_url) and index == 0:
                    if request:
                        instance.image_url = request.build_absolute_uri(pi.image.url)
                    else:
                        instance.image_url = pi.image.url
                    instance.save()
        return instance
