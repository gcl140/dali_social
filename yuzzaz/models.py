from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, verbose_name="Name")
    email = models.EmailField(unique=True, verbose_name="Official Email")
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True) #if none, call online avatar api
    about = models.TextField(max_length=100, blank=True, null=True)  # Placeholder field

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.username}"
