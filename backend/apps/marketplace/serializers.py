from rest_framework import serializers
from apps.marketplace.models import Post, PostImage, Cart, CartItem, Order, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    author_details = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'uuid', 'author', 'author_details', 'title', 'description', 
            'post_type', 'price', 'quantity', 'unit', 'location', 
            'is_active', 'images', 'uploaded_images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'author', 'created_at', 'updated_at']

    def get_author_details(self, obj):
        return {
            'username': obj.author.username,
            'email': obj.author.email,
            'first_name': obj.author.first_name,
            'last_name': obj.author.last_name,
        }

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        post = Post.objects.create(**validated_data)
        for image in uploaded_images:
            PostImage.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Ajouter de nouvelles images si fournies
        for image in uploaded_images:
            PostImage.objects.create(post=instance, image=image)
        return instance

class CartItemSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)
    post_price = serializers.DecimalField(source='post.price', max_digits=12, decimal_places=2, read_only=True)
    post_unit = serializers.CharField(source='post.unit', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'post', 'post_title', 'post_price', 'post_unit', 'quantity', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def get_total_price(self, obj):
        return sum(item.post.price * item.quantity for item in obj.items.all() if item.post.price)

class OrderSerializer(serializers.ModelSerializer):
    buyer_details = serializers.SerializerMethodField()
    seller_details = serializers.SerializerMethodField()
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Order
        fields = [
            'uuid', 'buyer', 'buyer_details', 'seller', 'seller_details', 
            'post', 'post_title', 'quantity', 'total_price', 'status', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'buyer', 'seller', 'total_price', 'created_at', 'updated_at']

    def get_buyer_details(self, obj):
        return {'username': obj.buyer.username, 'email': obj.buyer.email}

    def get_seller_details(self, obj):
        return {'username': obj.seller.username, 'email': obj.seller.email}

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'order', 'reviewer', 'reviewer_name', 'reviewee', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'reviewee', 'created_at']
