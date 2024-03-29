from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManger(BaseUserManager) :
    def create_user(self, email, password=None, **extra_fields) :
        """Create and save new user"""
        if not email :
            raise ValueError('You must have email')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self, email, password) :
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin) :
    """Custom user model promoted using email"""
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    objects = UserManger()
    USERNAME_FIELD = 'email'
