# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from base64 import decodestring as b64decode
from subprocess import Popen, PIPE

from qrcode import make as make_qrcode
from PIL import Image

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
    img_data = request.POST.get("img")
    if img_data:
        temp_qrcode_filename = "qr_code.jpg"
        open(temp_qrcode_filename, "wb").write(b64decode(img_data))
        cmd = [r".\zbar\zbarimg.exe", temp_qrcode_filename]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        print out
        if out:
            return JsonResponse({"status": "ok", "data": out[len("QR-Code:"):]})
    elif "upload" in request.FILES:
        img = request.FILES["upload"]
        temp_qrcode_filename = "qr_code.jpg"
        open(temp_qrcode_filename, "wb").write(img.read())
        img = Image.open(temp_qrcode_filename)
        new_img = img.resize((400, 400), Image.ANTIALIAS)
        new_img.save(temp_qrcode_filename)
        cmd = [r".\zbar\zbarimg.exe", temp_qrcode_filename]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        print out
        if out:
            return HttpResponseRedirect(out[len("QR-Code:"):].strip())
        else:
            return HttpResponseRedirect("/%s/scan_qrcode"%(app_config.get("app_url")))

    return JsonResponse({"status": "failed", "data": ""})
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

@login_required
def detail(request, name):
    if request.method == "GET":
        table = MetaDao.get_table(name)
        ID = request.GET.get("ID", "")
        data = MetaDao.get_table_row(name, ID)
        key_values= zip(table["cols"], data[0]["value"])
        context = {
            'app': app_config,
            'table': table,
            'key_values': key_values,
            'user': request.COOKIES.get('name')}
        return render(request, "detail.html", context=context)
