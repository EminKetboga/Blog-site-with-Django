from cmath import log
from email.policy import HTTP
import http
from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
# Create your views here.
def register(request):

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)

        newUser.save()
        login(request,newUser)
        messages.success(request,"Başarıyla Kayıt Oldunuz.")

        

        return redirect("index")
    context = {
            "form" : form
        }
    return render(request,"register.html",context)
def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username  = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username,password = password)
        if user is None:
            messages.info(request,"Kullanıcı Adı yada Parola Hatalı!")
            return render(request,"login.html",context)
        messages.success(request,"Başarı İle Giriş Yaptınız!")
        login(request,user)
        return redirect("index")
    

    return render(request,"login.html",context)
def logoutUser(request):
    logout(request)
    messages.success(request,"Başarı ile Sistemden Çıkış Yapıldı!")
    return redirect("index")