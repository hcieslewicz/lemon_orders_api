from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Stock(models.Model):
    """Stock to be used for a order"""
    name = models.CharField(max_length=255, unique=True)
    isin = models.CharField(max_length=12, unique=True)
    symbol = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Order object"""
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE
    # )
    #
    class SideChoices(models.TextChoices):
        buy = 'buy', _('Buy')
        sell = 'sell', _('Sell')

    isin = models.CharField(max_length=12)
    limit_price = models.FloatField()
    side = models.CharField(max_length=4, choices=SideChoices.choices)
    valid_until = models.IntegerField()
    quantity = models.IntegerField()
