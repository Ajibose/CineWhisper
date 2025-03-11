from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Favourite, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = str(user.user_id)
        token['username'] = user.username 
        token['email'] = user.email
        token['is_verified'] = user.is_verified

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password', 'password2', 'profile_picture']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = User.objects.create(
                username=validated_data.get('username'),
                email=validated_data.get('email'),
                profile_picture=validated_data.get('profile_picture')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["user_id", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import FavouriteSerializer here to avoid circular imports
        from .serializers import FavouriteSerializer
        self.fields['favourites'] = FavouriteSerializer(many=True, read_only=True)


class FavouriteSerializer(serializers.ModelSerializer):
    """Serializer for the favourite model"""
    content_type = serializers.SlugRelatedField(
            queryset=ContentType.objects.filter(model__in=["movie", "tvshow"]),
            slug_field="model"
    )

    class Meta:
        model = Favourite
        fields = ["user", "content_type", "object_id", "added_at"]

    def validate(self, data):
        """Ensure that object_id exists in the specified content_type"""
        model_class = data["content_type"].model_class()
        if not model_class.objects.filter(id=data["object_id"]).exists():
            raise serializers.ValidationError("Invalid object_id: No matching movie or TV show found.")
        return data


