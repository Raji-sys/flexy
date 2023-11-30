from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .filters import *
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
import datetime
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import os
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from .decorators import  superuser_required
from django.contrib import messages


def user_is_in(user):
    return not user.is_authenticated


@method_decorator(user_passes_test(user_is_in, login_url='/'), name='dispatch')
class CustomLoginView(LoginView):
    template_name='login.html'
    success_url=reverse_lazy('/')


@login_required
def Index(request):
    return render(request, 'inventory/index.html')

def register(request):
    if request.method == 'POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            UserProfile.objects.create(user=new_user)
            return render(request, 'account/register_done.html',{'new_user':new_user})
        else:
            messages.error(request,'error')
            return render(request,'account/register.html',{'user_form':user_form})
    else:
        user_form=UserRegistrationForm()
        return render(request,'account/register.html',{'user_form':user_form})
    

@login_required
def Edit(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'your profile updated succesfully')
        else:
            messages.error(request, 'error updating your profile')
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html',{'user_form':user_form,'profile_form':profile_form})


@login_required
def User_list(request):
    users=User.objects.filter(is_active=True,is_superuser=False)
    return render(request, 'account/user/list.html',{'section': 'people','users': users})


@login_required
def User_detail(request,username):
    user=get_object_or_404(User,username=username,is_active=True)
    return render(request, 'account/user/detail.html',{'section': 'people','user': user})


@login_required
def Remove_user(request,user_id):
    user=get_object_or_404(UserProfile,id=user_id)
    if user.pollingunit==request.user.wardadminprofile.pollingunit or request.user.is_superuser:
        if request.method=='POST':
            user.delete()
            messages.success(request, 'user profile deleted succesfully')
            return redirect('profile')
        return render(request, 'users/delete_user.html',{'user':user})
    else:
        return HttpResponse(f"{request.user.first_name} {request.user.last_name}, you do not have permission")


@login_required
def Courses(request):
    # form=coursesearch(request.GET)
    courses=Course.objects.all().order_by('name')
    course_lead=UserProfile.objects.get(role__iexact='chairman')
    courses_count=Course.objects.all().count()
    users=UserProfile.objects.all().order_by('name')[:5]
    mc=users.count()
    # if form.is_valid():
    #     name=form.cleaned_data.get('name')
    #     if name:
    #         courses=courses.filter(name__icontains=name)

    return render(request, "members/course.html",{'courses':courses,'courses_count':courses_count,'course_lead':course_lead,'mc':mc,'userrs':users})


@login_required
def Course_list(request,course_name):
    # form=StateSearch(request.GET) 
    course=get_object_or_404(course, name__iexact=course_name)
    course_lead=UserProfile.objects.filter(role=course_name)        
    states=course.states.all().order_by('name')
    states_count=course.states.all().count()

    # if form.is_valid():
    #     name=form.cleaned_data.get('name')
    #     if name:
    #         states=states.filter(name__icontains=name)

    return render(request, "members/state.html",{'course':course,'states':states,'states_count':states_count,'course_lead':course_lead })