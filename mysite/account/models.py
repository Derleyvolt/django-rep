from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation   import gettext as _
from django.core.exceptions import ValidationError

#from .teste import CustomUserManager

# Create your models here.

# class CustomUser(AbstractUser):
#     email = models.EmailField(_('email address'), unique=True)

#     USERNAME_FIELD  = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email

def username_validator(username):
    if len(username) < 8:
        raise ValidationError(
            _('%(username)s is smaller than 8 characters'),
            params={'username': username},
        )

def password_validator(password):
    if len(password) < 5:
        raise ValidationError(
            _('%(password)s is smaller than 8 characters'),
            params={'password': password},
        )

class CustomUserModel(models.Model):
    username  = models.CharField(max_length=100, validators=[username_validator], unique=True)
    password  = models.CharField(max_length=100, validators=[password_validator])
    name      = models.CharField(max_length=100)

# class CustomUserManager(BaseUserManager):
    
#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError(_('Users must have an email address'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user