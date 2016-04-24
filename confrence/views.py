from django.shortcuts import render
from django.template.context_processors import request
from django.http.response import HttpResponse, HttpResponseRedirect
from confrence.models import RegisterForm, ConfrenceModel
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return HttpResponse("Hello");

@login_required
def home(request):
    org_confrences = ConfrenceModel.objects.filter(organizer_id=request.user.id)
    rev_confrences = ConfrenceModel.objects.all()
    return render(request,'home.html',{'org_confrences':org_confrences,'rev_confrences':rev_confrences})
    


def register(request):
    print 'in register'
    if request.method == 'POST':
        print 'in Post'
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            new_user = form.save(commit=False)
            raw_paswd = new_user.password
            new_user.set_password(raw_paswd)
            new_user.save()
            return HttpResponseRedirect('/user/login/')

    form = RegisterForm()            
    return render(request,'registration/register.html',{'form':form})
