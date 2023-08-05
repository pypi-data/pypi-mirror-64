import json
from slugify import slugify
from django.utils import timezone
from datetime import date, datetime
from django.db import models
from django.http import JsonResponse
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from .utils import (
    json_serial, photo_url_filter, middle_name_filter,
    upload_status_image,
)
# Create your models here.


class UserProfileManager(BaseUserManager):
    """Helps django work with our custom user manager."""

    def create_user(self, email, first_name, last_name, password=None):
        """Create a new user profile object."""

        if not email:
            raise ValueError('Users must have an email address')

        email =self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Create and saves a new super user password."""

        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class CustomUserProfile(AbstractBaseUser, PermissionsMixin):
    """Represent user profiles inside our system."""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_status_image, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def get_full_name(self):
        """Used to get users full name."""
        if self.middle_name == None:
            return f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def get_short_name(self):
        """Used to get a users short name."""

        return f"{self.first_name} {self.last_name}"

    def get_user_profile(self):
        """Used to get full user information."""
        print(self.date_joined)
        data = {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': middle_name_filter(self.middle_name),
            'photo': photo_url_filter(self.photo),
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,
            'last_login': str(self.last_login), #json.dumps(self.last_login, default=json_serial),
            'date_joined': str(self.date_joined), #json.dumps(self.date_joined, default=json_serial),
            'full_name': self.get_full_name(),
            'short_name': self.get_short_name(),
        }
        return json.dumps(data)


    def __str__(self):
        """Django uses this to convert an object to a string."""

        return self.email
