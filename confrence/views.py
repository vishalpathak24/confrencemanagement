from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.http.response import HttpResponse, HttpResponseRedirect
from confrence.models import RegisterForm, Confrence, Topic, Reviewr, Upload, Submission, ConfrenceEditForm,\
    Author, ReviewerEditForm, UploadForm, SubmissionForm, PaperSubmissionForm, PosterSubmissionForm,PaperSubmission, AssgReviewerForm,\
    ReviewForm
from django.contrib.auth.decorators import login_required
from urllib2 import HTTPRedirectHandler
from django.forms import formset_factory 
from django.forms.models import modelformset_factory, inlineformset_factory,\
    modelform_factory
from django.db.models.query import QuerySet
from django import forms
from Crypto.Random.random import choice
import datetime
from django.forms.widgets import Textarea, TextInput

# Create your views here.
def index(request):
    return render(request,'index.html',{});

@login_required
def home(request):
    # checking user is author 
    author = Author.objects.filter(user = request.user) 
    if author:
        return HttpResponseRedirect('/confrence/confrence_home/'+`author[0].confrence.id`)
    
    org_confrences = Confrence.objects.filter(organizer_id=request.user.id)
    if org_confrences:
        request.session['is-org']=True
    my_reviwers = Reviewr.objects.filter(user_id=request.user.id)
    rev_confrences = [ my_reviewer.confrence for my_reviewer in my_reviwers]
    all_confrences = Confrence.objects.all()
    return render(request,'home.html',{'org_confrences':org_confrences,'rev_confrences':rev_confrences,'all_confrences':all_confrences})
    


def register(request,confrenceid="-1"):    
    if request.method == 'POST':
        #return HttpResponse("in POST")
        form = RegisterForm(request.POST)
        if form.is_valid():
            if confrenceid != "-1":
                confrence = Confrence.objects.get(id=confrenceid)
                if confrence:
                    new_user = form.save(commit=False)
                    raw_paswd = new_user.password
                    new_user.set_password(raw_paswd)
                    new_user.save()
                    author = Author()
                    author.user = new_user
                    author.confrence = confrence
                    author.save()
            else:
                #Easy chair user registration
                new_user = form.save(commit=False)
                raw_paswd = new_user.password
                new_user.set_password(raw_paswd)
                new_user.save()            
            return HttpResponseRedirect('/user/login/')
    else:
        form = RegisterForm()
        if confrenceid == "-1":
            return render(request,'registration/register.html',{'form':form})
        else:
            return render(request,'registration/register.html',{'form':form,'confrenceid':confrenceid})
            
                
#Confrence specific Views

@login_required
def confrence_home(request,confrenceid="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    organizer = confrence.organizer
    pcChair = confrence.pcChair
    topics = confrence.topic_set.all()
    reviewrs= confrence.reviewr_set.all()
    user=request.user
    author_user=[]
    reviewr_user=[]
    #Changing options on Basis of user privilages
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
    is_auth = False
    if not(review_option or edit_option or user == pcChair):
        is_auth = True    
    if(confrence):
        return render(request,'confrence/home.html',{'confrence':confrence,'topics':topics,'organizer':organizer,'authors':author_user,'reviewrs':reviewrs,'edit_option':edit_option,'review_option':review_option,'user':user,'is_auth':is_auth,'pcChair':pcChair})  

        
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
"""
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
"""
@login_required
def reviewr_edit(request,confrenceid="-1",authorid="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    organizer = confrence.organizer
    user=request.user
    reviewerFormSet = inlineformset_factory(Confrence,Reviewr,form=ReviewerEditForm)#fields=('user','topics'))#,queryset={"topics":confrence.topic_set.all()})
    if(confrence and organizer == request.user):
        if request.method == 'POST':      
            formset=reviewerFormSet(request.POST, request.FILES,instance=confrence)#ReviewerEditForm('-1',user,request.POST)
            if formset.is_valid():
                formset.save()
                return  HttpResponseRedirect("/confrence/confrence_home"+"/"+`confrence.id`)
        else:
            formset=reviewerFormSet(form_kwargs={'confrence': confrence,'current_user':user},instance=confrence)#ReviewerEditForm(confrence,user)
              
        #form.fields['user'].queryset = form.fields['user'].queryset.exclude(username=user.username)
        #form.fields['user'].queryset = form.fields['user'].queryset.exclude(username='admin')
        return render(request,'confrence/revieweredit.html',{'formset':formset,'confrence':confrence})
    else:           
        return HttpResponseRedirect("/user/home")

@login_required
def reviewr_assg(request,confrenceid,topicid="-1"):
    if request.session['is-org']==True:
        confrence = Confrence.objects.get(id=confrenceid)
        if confrence and confrence.organizer.id == request.user.id:
            reviewrformset = modelformset_factory(Submission,fields={'id','title','type','reviewr'},widgets={'title':TextInput(attrs={'readonly':True}),'title':TextInput(attrs={'readonly':True}),'type':TextInput(attrs={'readonly':True})},extra=0)          
            if request.method == 'POST':#need to assign reviewer
                formset = reviewrformset(request.POST)
                if formset.is_valid():
                    formset.save()
                    return HttpResponseRedirect("/confrence/confrence_edit/assgnReviewr/"+`confrence.id`)
            else:
                if topicid != "-1":
                    to_review_list = confrence.submission_set.filter(topic_id = topicid,reviewed = False) 
                    formset = reviewrformset(queryset=confrence.submission_set.filter(topic_id = topicid,reviewed = False))
                    if to_review_list:
                        pass
                    else:
                        formset=-1
                    #return HttpResponse("for topic id"+topicid)
                else:
                    formset = False
                topics = confrence.topic_set.all()    
                return render(request,'confrence/assgreviewer.html',{'confrence':confrence,'formset':formset,'topics':topics,'confrenceid':confrenceid})
    
    return HttpResponseRedirect("/user/home") 


#Submission
def submissions_home(request):
    if request.session['review-confrence']: #reviewer viewing submissions for confrence
        confrenceid = request.session['review-confrence']
        myreviewr = Reviewr.objects.get(user_id=request.user.id,confrence_id = confrenceid)
        if myreviewr:
            topics = myreviewr.topics.all()
            #topicsid = [topic.id for topic in topics]
            #confrence = Confrence.objects.get(id = confrenceid)
            #to_review_list = confrence.submission_set.filter(topic__in = topics,reviewed = False)        
            to_review_list = myreviewr.submission_set.filter(reviewed=False)
            return render(request,'submission/home.html',{'to_review_list':to_review_list,'rev_topics':topics})    
    else:
        return HttpResponse("submission_home");

def submission_form(request,confrenceid="-1",submissiontype="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    user=request.user
    if submissiontype == "-1":
        return HttpResponse(" Form type is not correct")
    if request.method=="POST":
        if submissiontype == "1":
            form = PaperSubmissionForm(request.POST, request.FILES)
        if submissiontype == "2":
            form = PosterSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            aut = Author.objects.get(user=request.user)
            if aut:
                upload=form.save(commit=False)
                upload.author = aut
                upload.confrence = confrence
                upload.reviewed = False
                upload.status = "Submitted"
                upload.upl_date = datetime.date.today()
                upload.type = form.type
                upload.save()  
            return HttpResponseRedirect("/confrence/home"+"/"+`confrence.id`)
    else:
        if submissiontype == "1":
            form=PaperSubmissionForm()
        if submissiontype == "2":
            form=PosterSubmissionForm()
        form.fields['topic'].queryset = confrence.topic_set.all()
        return render(request,'confrence/upload.html',{'form':form,'confrence':confrence,'submissiontype':submissiontype})
    return HttpResponse("this is not good"+str(submissiontype)+str(submissiontype == "1"))
    
@login_required   
def submissions_review(request,subid="-1"):  
    if subid != "-1":
        submission = Submission.objects.get(id=subid)
        if submission.reviewr.user == request.user:
            if request.method == 'POST':
                form = ReviewForm(request.POST,request.FILES)
                if form.is_valid():
                    myreviewr = Reviewr.objects.get(user_id=request.user.id,confrence_id = submission.confrence.id)
                    review = form.save(commit=False)
                    review.submission = submission
                    review.reviewr = myreviewr
                    review.save()
                    submission.reviewed = True
                    submission.status = "Reviewed"
                    submission.save() 
                    return redirect('submissions-home')
            else:
                
                form = ReviewForm()
                return render(request,'submission/addreview.html',{'form':form,'submissionid':submission.id})    
    return redirect('submissions-home')

def view_file1(request,confrenceid="-1"):
    confrence = Confrence.objects.get(id=confrenceid)
    user=request.user
    subconfrence = Submission.objects.all()
    return render(request,'confrence/download.html',{"confrence":confrence,"subconfrence":subconfrence,"user":user})

def view_file(request,submissionid="-1"):
    if submissionid == "-1":
        return HttpResponse("sorry this file not found")
    else:
        fls=Submission.objects.get(id=submissionid)
        filename = fls.subFile.name.split('/')[-1]
        response = HttpResponse(fls.subFile, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
