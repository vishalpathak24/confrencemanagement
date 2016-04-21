from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm

# Create your models here.
    

class ConfrenceModel(models.Model):
    confrenceName = models.CharField(max_length=30)
    oraganiser = models.ForeignKey(User,on_delete = models.SET_NULL,null=True)
    
    startDate = models.DateField(blank=False)
    endDate = models.DateField(blank=False)
    
    def __str__(self):
        return self.confrenceName

class Reviewr(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE) #removes User from reviewers
    confrence = models.ForeignKey(ConfrenceModel,on_delete = models.CASCADE)
    def __str__(self):
        return self.user.username
    


#Registration form for user
class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
    