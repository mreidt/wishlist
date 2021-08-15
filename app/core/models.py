import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Produto(models.Model):
    """Produto model that stores product informations"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    price = models.FloatField()
    image = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    review_score = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.title


class WishlistItem(models.Model):
    """Wishlist item model that stores clients wishlists"""
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Produto, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.client}/{self.product}'
