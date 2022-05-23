from locale import normalize
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
# from django.utils.translation import gettext_lazy as _


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)        
        return user

    def create_superuser(self, email,  password=None, **other_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)        
        other_fields.setdefault('is_active', True)
        
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        
        
        user = self.create_user(
            email,
            password=password,
            **other_fields
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login	= models.DateTimeField(verbose_name='last login', auto_now=True)
    
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    # def email_user(self, subject, message):
    #     send_mail(
    #         subject,
    #         message,
    #         'l@1.com',
    #         [self.email],
    #         fail_silently=False,
    #     )
################################################################################################





# class MyUserManager(BaseUserManager):
    
    
#     def create_user(self, email, password=None, **other_fields):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         # other_fields.setdefault('is_staff', False)

#         if not email:
#             raise ValueError('Users must have an email address')

#         email = self.normalize_email(email)
#         user = self.model(email=email, **other_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, **other_fields):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)        
#         other_fields.setdefault('is_active', True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_staff=True.')
#         if other_fields.get('is_superuser') is not True:
#             raise ValueError(
#                 'Superuser must be assigned to is_superuser=True.')
        

#         # user = self.create_user(
#         #     email=email,
#         #     password=password,
#         #     **other_fields,
#         #     
#         # )
#         # user.is_admin = True
#         # user.save(using=self._db)
#         # return user
#         return self.create_user(email, password, **other_fields)

    


# class MyUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     # date_of_birth = models.DateField()
#     date_joined = models.DateTimeField(
#         verbose_name='date joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)

#     objects = MyUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.email

#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.email

#     def __str__(self):              # __unicode__ on Python
#         return self.email

#     # def has_perm(self, perm, obj=None):
#     #     "Does the user have a specific permission?"
#     #     # Simplest possible answer: Yes, always
#     #     return True

#     # def has_module_perms(self, app_label):
#     #     "Does the user have permissions to view the app `app_label`?"
#     #     # Simplest possible answer: Yes, always
#     #     return True

#     # @property
#     # def is_staff(self):
#     #     "Is the user a member of staff?"
#     #     # Simplest possible answer: All admins are staff
#     #     return self.is_admin
