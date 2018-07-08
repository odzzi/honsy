# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms
from meta_dao import MetaDao
# Create your views here.


def user_login(request):
    class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField()
    sessionid = request.COOKIES.get('sessionid')
    if sessionid:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            # user = Profile.objects.filter(nick_name=username,password=password)
            # =================认证开始====================
            user = authenticate(username=username,password=password)
            # =================认证结束====================
            if user:
             # =================登录====================
                login(request,user)
             #
                response = HttpResponseRedirect('/')
                response.set_cookie('name', username, 60*60*24*1)
                return response
                # return render(request,'feedback.html')
                # 这里直接写模版渲染，就不能设置cookie的过期时间了
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.set_cookie('name', None)
    return response

@login_required
def honsy(request):
    tables = MetaDao.list_tables()
    context = {'tables': tables }
    return render(request, "honsy.html", context=context)

@login_required
def list(request, name):
    table = MetaDao.get_table(name)
    data = MetaDao.get_table_data(name)
    context = {'table': table,  'data': data }
    return render(request, "list.html", context=context)

@login_required
def edit(request, path):
    tables = MetaDao.list_tables()
    context = {'tables': tables }
    return render(request, "edit.html", context=context)

@login_required
def add(request, name):
    if request.method == "GET":
        table = MetaDao.get_table(name)
        context = {'table': table}
        return render(request, "add.html", context=context)
    else:
        table = MetaDao.get_table(name)
        cols = []
        for col in table.get("cols", []):
            cols.append(request.POST.get(col))
        MetaDao.add_table_row(name, cols)
        return  HttpResponseRedirect("/honsy/list/%s"%name)