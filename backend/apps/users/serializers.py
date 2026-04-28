"""
apps/users/serializers.py
-------------------------
Serializers pour l'authentification et les profils utilisateurs.
"""
from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer complet — lecture/écriture du profil utilisateur."""
    spaces = serializers.DictField(source='get_spaces', read_only=True)
    organisations_created = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'uuid', 'username', 'email',
            'first_name', 'last_name', 'password',
            'is_staff', 'role', 'spaces', 'organisations_created',
            'date_joined'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
            'role': {'read_only': True},
            'date_joined': {'read_only': True},
        }

    def get_organisations_created(self, obj):
        return [{'uuid': str(o.uuid), 'name': o.name} for o in obj.organisations_created.all()]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserSignupSerializer(serializers.ModelSerializer):
    """Serializer d'inscription — crée un compte utilisateur."""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'first_name', 'last_name', 'password', 'role']
        read_only_fields = ['uuid']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role'),
        )


class MobileSignupSerializer(serializers.ModelSerializer):
    """
    Serializer d'inscription mobile.
    Crée un compte INACTIF (is_active=False) qui sera activé
    uniquement après vérification du code OTP envoyé par email.
    """
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'first_name', 'last_name', 'password', 'role']
        read_only_fields = ['uuid']

    def validate_role(self, value):
        valid_roles = [c[0] for c in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Rôle invalide. Valeurs acceptées : {', '.join(valid_roles)}"
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role'),
            is_active=False,  # Compte inactif jusqu'à validation OTP
        )
        return user


class UserLoginSerializer(serializers.Serializer):

    """
    Serializer de connexion.
    Accepte 'email' ou 'username' pour une compatibilité maximale avec le frontend.
    """
    email    = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('email') or data.get('username')
        password = data.get('password')

        if not identifier:
            raise serializers.ValidationError("L'email ou le nom d'utilisateur est requis.")

        user = authenticate(username=identifier, password=password)
        if not user:
            raise serializers.ValidationError("Identifiants invalides")
        
        data['user'] = user
        return data


class FarmerDirectorySerializer(serializers.ModelSerializer):
    """
    Serializer pour l'annuaire de découverte des agriculteurs.
    Agrège les informations sur les parcelles et les cultures.
    """
    total_area = serializers.SerializerMethodField()
    crops      = serializers.SerializerMethodField()
    location   = serializers.SerializerMethodField()
    # ✅ AJOUTÉ : permet au frontend de vérifier le type de compte si besoin
    spaces     = serializers.DictField(source='get_spaces', read_only=True)

    class Meta:
        model = User
        fields = [
            'uuid', 'username', 'email', 'first_name', 'last_name',
            'total_area', 'crops', 'location',
            'spaces',  # ✅ AJOUTÉ
        ]

    def get_total_area(self, obj):
        from django.db.models import Sum
        return obj.parcels.aggregate(total=Sum('parcel_crops__area'))['total'] or 0.0

    def get_crops(self, obj):
        from apps.crops.models import ParcelCrop
        return list(
            ParcelCrop.objects.filter(parcel__owner=obj)
            .values_list('crop__name', flat=True)
            .distinct()
        )

    def get_location(self, obj):
        parcel = obj.parcels.first()
        return parcel.get_center() if parcel else None