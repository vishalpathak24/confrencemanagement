from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.template.defaultfilters import default

# Create your models here.
 


class Confrence(models.Model):
    confrenceName = models.CharField(max_length=30)
    organizer = models.ForeignKey(User,on_delete = models.SET_NULL,null=True)
    
    startDate = models.DateField(blank=False)
    endDate = models.DateField(blank=False)
        
    def __str__(self):
        return self.confrenceName

class Topic(models.Model):
    topicName = models.CharField(max_length=30)
    confrence = models.ForeignKey(Confrence,on_delete = models.CASCADE,null=True)    
    def __str__(self):
        return self.topicName    

class Reviewr(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE) #removes User from reviewers
    confrence = models.ForeignKey(Confrence,on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete = models.CASCADE)
    #def clean(self):
        #only confrence having topic must be added
        
    def __str__(self):
        return "Reviewer of"+self.confrence.__str__()+" "+self.user.first_name+" "+self.user.last_name
    


#Registration form for user
class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']

#Confrence Editing form for Organizer
class ConfrenceEditForm(ModelForm):
    class Meta:
        model = Confrence
        fields = ['confrenceName','startDate','endDate']
    