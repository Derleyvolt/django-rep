from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, AbstractBaseUser
from django.utils.translation   import gettext as _
from django.core.exceptions import ValidationError
from .teste import UserManager

class CustomUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)   
    staff     = models.BooleanField(default=False) # a admin user; non super-user
    admin     = models.BooleanField(default=False) # a superuser

    objects = UserManager()

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] # Username & Password are required by default.

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin