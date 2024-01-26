# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from apps.home.forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth.models import User

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        if load_template == 'page-user.html':
            if request.method == 'POST':
                user_form = UpdateUserForm(request.POST, instance=request.user)
                profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    profile_form.save()
                    messages.success(request, 'Your profile is updated successfully')
                    return redirect('home/page-user.html')
                else:
                    return render(request, "home/page-user.html", {'user_form':user_form, 'profile_form':profile_form,'current_user':request.user,'segment':load_template})  
            else:
                user_form = UpdateUserForm(instance=request.user)
                profile_form = UpdateProfileForm(instance=request.user.profile)
                context['user_form'] = user_form
                context['profile_form'] = profile_form
                context['current_user'] = request.user
                context['segment'] = load_template
                html_template = loader.get_template('home/page-user.html')
                return HttpResponse(html_template.render(context, request))
        if load_template == 'page-list-users.html':
            list_users = User.objects.all()
            context['count'] = list_users.count()
            context['staff'] = list_users.filter(is_staff = True).count()
            context['inactive'] = list_users.filter(is_active = False).count()
            context['list_users'] = list_users
            context['segment'] = load_template
            html_template = loader.get_template('home/page-list-users.html')
            return HttpResponse(html_template.render(context, request))

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
 
    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



