from django.shortcuts import render
from django.template.context_processors import request
from django.http.response import HttpResponse, HttpResponseRedirect
from confrence.models import RegisterForm, Confrence, Topic, ConfrenceEditForm,\
    Author, AuthorEditForm
from django.contrib.auth.decorators import login_required
from urllib2 import HTTPRedirectHandler
from django.forms.models import modelformset_factory, inlineformset_factory,\
    modelform_factory
from django.db.models.query import QuerySet
from django import forms
from Crypto.Random.random import choice

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
    author_user=[]
    if authors:
        for author in authors:
            author_user.append(author.user) #if author exist find user for this author
        authors = author_user #if author exist find user for this author
    edit_option = False;
    if(organizer == request.user):
        edit_option=True;
    if(confrence):
        return render(request,'confrence/home.html',{'confrence':confrence,'topics':topics,'organizer':organizer,'authors':author_user,'edit_option':edit_option})  
        
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
            form=AuthorEditForm(request.POST)
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