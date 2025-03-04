from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import uuid

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    # Override the fields to remove them.
    first_name = None
    last_name = None

    user_id  = models.UUIDField(
            primary_key=True, default=uuid.uuid4,
            editable=False
    )
    
    profile_picture = models.ImageField(
            upload_to="profile_pictures/",
            blank=True, null=True
    )
    
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        """String representation of instances"""
        return f"{self.username}"


class Favourite(models.Model):
    """
    Model to store user's favorite movies or TV shows
    """
    favourite_id = models.UUIDField(
            primary_key=True, default=uuid.uuid4,
            editable=False
    )
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='favourites'
    )
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "content_type", "object_id"]

    def clean(self):
        """Validate that object_id is a valid instance of content_type"""
        model_class = self.content_type.model_class()
        if not model_class.objects.filter(id=self.object_id).exists():
            raise ValidationError("Invalid object_id: No matching movie or TV show found.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user} - {self.content_object}"
