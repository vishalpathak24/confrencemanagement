from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm

# Create your models here.

#Registration form for user
class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
    