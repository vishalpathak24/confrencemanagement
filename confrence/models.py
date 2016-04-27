from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.template.defaultfilters import default
from django import forms
from twisted.protocols.amp import MAX_VALUE_LENGTH
# Create your models here.
 


class Confrence(models.Model):
    confrenceName = models.CharField(max_length=30)
    organizer = models.ForeignKey(User,on_delete = models.SET_NULL,null=True)
    pcChair = models.ForeignKey(User,on_delete = models.SET_NULL,related_name='+',null=True,blank=True)
    startDate = models.DateField(blank=False)
    endDate = models.DateField(blank=False)
    notifyDate = models.DateField(blank=False,null=True)    
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
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name+" Author of"+self.confrence.__str__()  

class Upload(models.Model):
    fl = models.FileField(upload_to="files/")  
    name= models.CharField(max_length=30) 
    upl_date= models.DateField(blank=False)


    
class Reviewr(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE) #removes User from reviewers
    confrence = models.ForeignKey(Confrence,on_delete = models.CASCADE)
    topics = models.ManyToManyField(Topic)
    #def clean(self):
        #only confrence having topic must be added
        
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

class Submission(models.Model):
    confrence = models.ForeignKey(Confrence,on_delete = models.CASCADE)
    author = models.ForeignKey(Author,on_delete = models.CASCADE,null=True)
    title = models.CharField(max_length=30,null=True)
    status = models.CharField(max_length=30,null=True)
    subFile = models.FileField(upload_to="files/",null=True)
    upl_date= models.DateField(null=True)#blank=False,null=True)
    topic = models.ForeignKey(Topic,on_delete = models.CASCADE,null=True)
    reviewed = models.BooleanField(default=False)
    type = models.CharField(max_length=30,null=True)
    reviewr = models.ForeignKey(Reviewr,on_delete = models.SET_NULL,null=True)
    acceptance = models.BooleanField(default=False)
    final_comment = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.title+" "+self.author.user.first_name+" "+self.confrence.__str__()

class PaperSubmission(Submission):
    filesize=models.IntegerField(null=True)
    
class PosterSubmission(Submission):
    filesize=models.IntegerField(null=True)  
    def getType(self):
        return type

class Review(models.Model):
    submission = models.ForeignKey(Submission,on_delete = models.CASCADE)
    reviewr = models.ForeignKey(Reviewr,on_delete = models.CASCADE)
    comment = models.CharField(max_length=30)
    score = models.IntegerField()


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
"""
class AuthorEditForm(ModelForm):
    def __init__(self,confrence, *args, **kwargs):
        super(AuthorEditForm, self).__init__(*args, **kwargs)
	if confrence != '-1':
        	self.fields['topics']=forms.ModelMultipleChoiceField(queryset=confrence.topic_set.all(),widget=forms.CheckboxSelectMultiple(),required=True)
    class Meta:
        model = Author
        fields=['user','topics']

"""
class ReviewerEditForm(ModelForm):
        
    def __init__(self, *args, **kwargs):
        confrence = "-1"
        if 'confrence' in kwargs:
            confrence = kwargs.pop('confrence')
            current_user = kwargs.pop('current_user')
            
        super(ReviewerEditForm,self).__init__(*args, **kwargs)
        if confrence != '-1':
            self.fields['topics']=forms.ModelMultipleChoiceField(queryset=confrence.topic_set.all(),widget=forms.CheckboxSelectMultiple(),required=True)
            self.fields['user'].queryset = self.fields['user'].queryset.exclude(id=current_user.id)
        
    class Meta:
        model = Reviewr
        fields=['user','topics']
    
    

class UploadForm(ModelForm):
    class Meta:
        model=Upload
        fields=['name','fl']

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['subFile','title','topic']

class PaperSubmissionForm(ModelForm):
    type="Paper"
    class Meta:
        model = PaperSubmission
        fields = ['subFile','title','topic']

class PosterSubmissionForm(ModelForm):
    type="Poster"
    class Meta:
        model = PosterSubmission
        fields = ['subFile','title','topic']

class AssgReviewerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssgReviewerForm, self).__init__(*args,**kwargs)
        self.fields['title'].widget.attrs['readonly'] = True
        self.fields['topic'].widget.attrs['readonly'] = True
        self.fields['type'].widget.attrs['readonly'] = True
        
    class Meta:
        model = Submission
        fields = ['id','title','topic','type','reviewr']

class ReviewForm(ModelForm): 
    class Meta:
        model=Review
        fields=['comment','score']

class PcChairAssignForm(ModelForm):
    class Meta:
        model = Confrence
        fields = ['pcChair']
