from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from apps.userprofile.models import Profile, ProfileGenerated

class admin_user(models.Model):
    UserName = models.CharField(max_length=12 )
    Password = models.CharField(max_length=12 )
    def __str__(self):
        return self.name