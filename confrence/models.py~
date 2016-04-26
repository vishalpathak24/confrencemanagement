from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.template.defaultfilters import default
from django import forms
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

class Author(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    confrence = models.ForeignKey(Confrence,on_delete = models.CASCADE)
    topics = models.ManyToManyField(Topic)
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name+" Author of"+self.confrence.__str__()  
    
class Reviewr(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE) #removes User from reviewers
    confrence = models.ForeignKey(Confrence,on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete = models.CASCADE)
    #def clean(self):
        #only confrence having topic must be added
        
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name+"Reviewer of"+self.confrence.__str__()
    


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


class AuthorEditForm(ModelForm):
    def __init__(self,confrence, *args, **kwargs):
        super(AuthorEditForm, self).__init__(*args, **kwargs)
        self.fields['topics']=forms.ModelMultipleChoiceField(queryset=confrence.topic_set.all(),widget=forms.CheckboxSelectMultiple(),required=True)
    class Meta:
        model = Author
        fields=['user','topics']
    