from django.shortcuts import render
from django.template.context_processors import request
from django.http.response import HttpResponse, HttpResponseRedirect
from confrence.models import RegisterForm, Confrence, Topic, ConfrenceEditForm
from django.contrib.auth.decorators import login_required
from urllib2 import HTTPRedirectHandler
from django.forms.models import modelformset_factory, inlineformset_factory
from django.db.models.query import QuerySet

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
    edit_option = False;
    if(organizer == request.user):
        edit_option=True;
    if(confrence):
        return render(request,'confrence/home.html',{'confrence':confrence,'topics':topics,'organizer':organizer,'edit_option':edit_option})  
        
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
