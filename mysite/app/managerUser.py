from django.contrib.auth.models import BaseUserManager
from django.utils.translation   import gettext as _
from django.contrib.auth.hashers      import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, password, documento=None, username=None):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.username  = username
        user.documento = documento

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
