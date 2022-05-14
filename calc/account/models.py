from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, AbstractUser
    
)

# Create your models here.

class User(AbstractBaseUser):
    email   = models.EmailField(max_length= 255, unique=True)
    active  = models.BooleanField(default=True) # can login
    staff   = models.BooleanField(default= True) # staff user not superuser
    admin   = models.BooleanField(default=False) #superuser
    
    
    USERNAME_FIELD = 'email'
    
    
    REQUIRED_FIELDS: []
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active
 
class Profile(models.Model):
    user = models.ForeignKey(User)