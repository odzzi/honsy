# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from qrcode import make as make_qrcode, QRCode
import json

from django.shortcuts import render, HttpResponseRedirect
from django.http import FileResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms
from meta_dao import MetaDao
# Create your views here.


app_config = json.load(open(r"./conf/app.json"))

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
    return render(request, 'login.html', context={'app': app_config})


def user_logout(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.set_cookie('name', None)
    return response

@login_required
def index(request):
    tables = MetaDao.list_tables()
    context = {
        'app': app_config,
        'tables': tables,
        'user': request.COOKIES.get('name')}
    return render(request, "honsy.html", context=context)

@login_required
def list(request, name):
    table = MetaDao.get_table(name)
    data = MetaDao.get_table_data(name)
    context = {
        'app': app_config,
        'table': table,
        'data': data,
        'user': request.COOKIES.get('name')}

    return render(request, "list.html", context=context)

@login_required
def edit(request, path):
    tables = MetaDao.list_tables()
    context = {
        'app': app_config,
        'tables': tables,
        'user': request.COOKIES.get('name')}
    return render(request, "edit.html", context=context)

@login_required
def show_qrcode(request):
    msg = request.GET.get("msg")
    context = {
        'app': app_config,
        'msg': msg,
        'user': request.COOKIES.get('name')}
    return render(request, "show_qrcode.html", context=context)

@login_required
def scan_qrcode(request):
    context = {
        'app': app_config,
        'user': request.COOKIES.get('name')}
    return render(request, "scan_qrcode.html", context=context)

@login_required
def decode_qrcode(request):

    return JsonResponse({"status":"ok", "data":"123456"})

@login_required
def get_qrcode(request):
    msg = request.GET.get("msg")
    # 这个二维码信息，可以转换为文件流，不用保存为文件再读取。这个是临时做法。
    qr_img = make_qrcode(msg)
    qr_img.save("./test.png")
    return FileResponse(open(r"./test.png", "rb"), content_type="image/png")

@login_required
def add(request, name):
    if request.method == "GET":
        table = MetaDao.get_table(name)
        context = {
            'app': app_config,
            'table': table,
            'user': request.COOKIES.get('name')}
        return render(request, "add.html", context=context)
    else:
        table = MetaDao.get_table(name)
        cols = []
        for col in table.get("cols", []):
            cols.append(request.POST.get(col))
        MetaDao.add_table_row(name, cols)
        return  HttpResponseRedirect("/%s/list/%s"%(app_config.get("app_url"), name))