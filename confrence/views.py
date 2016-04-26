from django.shortcuts import render
from django.template.context_processors import request
from django.http.response import HttpResponse, HttpResponseRedirect
from confrence.models import RegisterForm, Confrence, Topic, Upload, ConfrenceEditForm,\
    Author, AuthorEditForm, ReviewerEditForm, UploadForm
from django.contrib.auth.decorators import login_required
from urllib2 import HTTPRedirectHandler
from django.forms.models import modelformset_factory, inlineformset_factory,\
    modelform_factory
from django.db.models.query import QuerySet
from django import forms
from Crypto.Random.random import choice
import datetime

# Create your views here.
def index(request):
    return HttpResponse("Hello");

@login_required
def home(request):
    org_confrences = Confrence.objects.filter(organizer_id=request.user.id)
    all_confrences = Confrence.objects.all()
    return render(request,'home.html',{'org_confrences':org_confrences,'all_confrences':all_confrences})
    


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            new_user = form.save(commit=False)
            raw_paswd = new_user.password
            new_user.set_password(raw_paswd)
            new_user.save()
            return HttpResponseRedirect('/user/login/')

    form = RegisterForm()            
    return render(request,'registration/register.html',{'form':form})


#Confrence specific Views

@login_required
def confrence_home(request,confrenceid="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    organizer = confrence.organizer
    topics = confrence.topic_set.all()
    authors = confrence.author_set.all()
    reviewrs= confrence.reviewr_set.all()
    user=request.user
    author_user=[]
    reviewr_user=[]
    #Changing options on Basis of user privilages
    is_auth=False
    if authors:
        for author in authors:
            if author.user.username == user.username:
                is_auth=True
            author_user.append(author.user) #if author exist find user for this author
        authors = author_user #if author exist find user for this author
    
    review_option = False;
    if reviewrs:	
        for reviewr in reviewrs:
            reviewr_user.append(reviewr.user)
            if (reviewr.user == request.user):
                review_option = True
                request.session['review-confrence']=confrence.id #Setting Session for confrence
        reviewrs= reviewr_user
    
    edit_option = False;
    if(organizer == request.user):
        edit_option=True;
        request.session['org-confrence']=confrence.id #Setting Session for confrence
    
    if(confrence):
        return render(request,'confrence/home.html',{'confrence':confrence,'topics':topics,'organizer':organizer,'authors':author_user,'reviewrs':reviewrs,'edit_option':edit_option,'review_option':review_option,'user':user,'is_auth':is_auth})  
        
    return HttpResponseRedirect("/user/home")

@login_required
def confrence_edit(request,confrenceid="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    organizer = confrence.organizer
    TopicFormset = inlineformset_factory(Confrence,Topic,fields=('topicName',))#fields={'confrenceName','startDate','endDate'}
    if(confrence):
        if(organizer == request.user):
            #User is organizer of confrence
            if request.method == 'POST':
                confrenceform = ConfrenceEditForm(request.POST)
                topicformset = TopicFormset(request.POST, request.FILES, instance=confrence)
                if topicformset.is_valid() and confrenceform.is_valid():
                    confrence_new = confrenceform.save(commit=False)
                    confrence_new.id = confrence.id
                    confrence_new.organizer = organizer
                    confrence_new.save()
                    topicformset.save()
                    return  HttpResponseRedirect("/confrence/home"+"/"+`confrence.id`)
                
            else:
                confrenceform = ConfrenceEditForm(initial={'confrenceName':confrence.confrenceName,'startDate':confrence.startDate,'endDate':confrence.endDate})
                topicformset = TopicFormset(instance = confrence)
            return render(request,'confrence/edit.html',{'confrenceform':confrenceform,'topicformset':topicformset,'confrence':confrence})
        
        
    return HttpResponseRedirect("/user/home")

@login_required
def author_edit(request,confrenceid="-1",authorid="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    organizer = confrence.organizer
    #author_form=modelform_factory(Author,fields={'user','topics'},widgets={"topics":forms.CheckboxSelectMultiple()})
    #author_form.topics = forms.ChoiceField(widget=forms.CheckboxSelectMultiple(),required=True,choices=topics)
    #print author_form
    if(confrence and organizer == request.user):
        if request.method == 'POST':      
            #form=author_form(request.POST)
            form=AuthorEditForm('-1',request.POST)
            if form.is_valid():
                author = form.save(commit=False)
                author.confrence = confrence
                author.save()
                return  HttpResponseRedirect("/confrence/home"+"/"+`confrence.id`)
        else:
            #form=author_form()
            form=AuthorEditForm(confrence=confrence)
        #form.topics=forms.ChoiceField(widget=forms.CheckboxSelectMultiple(),required=True,choices=topics)
        #form.topics(widget=forms.CheckboxSelectMultiple(),required=True)
        return render(request,'confrence/authoredit.html',{'form':form,'confrence':confrence})
    else:           
        return HttpResponseRedirect("/user/home")

@login_required
def reviewr_edit(request,confrenceid="-1",authorid="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    organizer = confrence.organizer
    user=request.user
    if(confrence and organizer == request.user):
        if request.method == 'POST':      
            form=ReviewerEditForm('-1',user,request.POST)
            if form.is_valid():
                reviewr = form.save(commit=False)
                reviewr.confrence = confrence
                reviewr.save()
                return  HttpResponseRedirect("/confrence/home"+"/"+`confrence.id`)
        else:
            form=ReviewerEditForm(confrence,user)
               
        form.fields['user'].queryset = form.fields['user'].queryset.exclude(username=user.username)
        form.fields['user'].queryset = form.fields['user'].queryset.exclude(username='admin')
        return render(request,'confrence/revieweredit.html',{'form':form,'confrence':confrence})
    else:           
        return HttpResponseRedirect("/user/home")

#Submission
def submission_home(request):
    return HttpResponse("Submission Home");

def submission_form(request,confrenceid="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    got=1
    if request.method=="POST":
        form = UploadForm(request.POST, request.FILES) 
	got=form.is_valid()      
        if form.is_valid():
	    upload=form.save(commit=False)
            upload.upl_date=datetime.date.today()
            upload.save()  
            return HttpResponseRedirect("/confrence/home"+"/"+`confrence.id`)
    form=UploadForm()
    return render(request,'confrence/upload.html',{'form':form,'confrence':confrence,'got':got})

def view_file1(request):
    return render(request,'confrence/download.html',{})

def view_file(request):
    fls=Upload.objects.get(name="first")
    filename = fls.fl.name.split('/')[-1]
    response = HttpResponse(fls.fl, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
	
