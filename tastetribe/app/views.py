from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings   
import math,random


# Create your views here.
def shop_login(req):
    if 'user' in req.session:
        return redirect(home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['passwd']
        data=authenticate(username=uname,password=password)
        if data:
                req.session['user']=uname   #create session
                return redirect(home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(shop_login)
    
    else:
        return render(req,'login.html')
    
def shp_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(shop_login)
    
def OTP(req):
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        otp=OTP(req)
        if User.objects.filter(email=email).exists():
            messages.error(req, "Email is already in use.")
            return redirect(register)
        else:
            send_mail('Your registration OTP ,',f"OTP for registration is {otp}", settings.EMAIL_HOST_USER, [email])
            messages.success(req, "Registration successful. Please check your email for OTP.")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'register.html')

def validate(req,name,password,email,otp):
    if req.method=='POST':
        uotp=req.POST['uotp']
        if uotp==otp:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            messages.success(req, "OTP verified successfully. You can now log in.")
            return redirect(shop_login)
        else:
            messages.error(req, "Invalid OTP. Please try again.")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'validate.html',{'name':name,'pass':password,'email':email,'otp':otp})






def home(req):
    if 'user' in req.session:
        dish=Dish.objects.all()
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        return render(req,'home.html',{'dish':dish,'ingr':ingr,'cook':cook})
    else:
        return redirect(shop_login)
    
def profile(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        dish=Dish.objects.filter(user=user)
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        return render(req,'profile.html',{'dish':dish,'ingr':ingr,'cook':cook})
    else:
        return redirect(shop_login)
    
def addRecipe(req):
    if 'user' in req.session:
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            img=req.FILES['img']
            cuisine=req.POST['cuisine']
            prep=req.POST['prep']
            cook=req.POST['cook']
            data=Dish.objects.create(user=user,name=name,img=img,cuisine=cuisine,prep=prep,cook=cook,likes=0,rating=0)
            data.save()
            pk=data.pk
            return redirect("ingredients",pid=pk)
        else:
            return render(req,'addRecipe.html')
    else:
        return redirect(shop_login)
    
def ingredients(req,pid):
    if 'user' in req.session:
        if req.method=='POST':
            ingr=req.POST['ingredients']
            data=Ingredients.objects.create(dish=Dish.objects.get(id=pid),item=ingr)
            data.save()
            return redirect('ingredients',pid=pid)
        else:
            dish=Dish.objects.get(pk=pid)
            data=Ingredients.objects.filter(dish=dish)
            return render(req,'ingredients.html',{'data':data,'dish':dish})
    else:
        return redirect(shop_login)
    
def cooking(req,pid):
    if 'user' in req.session:
        if req.method=='POST':
            steps=req.POST['steps']
            data=Cooking.objects.create(dish=Dish.objects.get(id=pid),steps=steps)
            data.save()
            return redirect('cooking',pid=pid)
        else:
            dish=Dish.objects.get(pk=pid)
            data=Cooking.objects.filter(dish=dish)
            return render(req,'cooking.html',{'data':data,'dish':dish})
    else:
        return redirect(shop_login)
    
def edit(req,pid):
    if 'user' in req.session:
        if req.method=='POST':
            name=req.POST['name']
            img=req.FILES.get('img')
            cuisine=req.POST['cuisine']
            prep=req.POST['prep']
            cook=req.POST['cook']
            if img:
                Dish.objects.filter(pk=pid).update(name=name,cuisine=cuisine,prep=prep,cook=cook)
                data=Dish.objects.get(pk=pid)
                url=data.img.url
                og_path=url.split('/')[-1]
                os.remove('media/'+og_path)
                data.img=img
                data.save()
            else:
                Dish.objects.filter(pk=pid).update(name=name,cuisine=cuisine,prep=prep,cook=cook)
            return redirect('edit',pid=pid)
        else:
            data=Dish.objects.get(pk=pid)
            return render(req,'edit.html',{'data':data})
    else:
        return redirect(shop_login)
    
def editIngr(req,pid):
    if 'user' in req.session:
        if req.method=='POST':
            ingr=req.POST['ingredients']
            Ingredients.objects.filter(pk=pid).update(item=ingr)
            data=Ingredients.objects.get(pk=pid)
            return redirect('ingredients',pid=data.dish.pk)
        else:
            data=Ingredients.objects.get(pk=pid)
            return render(req,'editIngr.html',{'data':data})
    else:
        return redirect(shop_login)
    
def deleteIngr(req,pid):
    if 'user' in req.session:
        data=Ingredients.objects.get(pk=pid)
        dId=data.dish.pk
        data.delete()
        return redirect('ingredients',pid=dId)
    else:
        return redirect(shop_login)
    
def editCook(req,pid):
    if 'user' in req.session:
        if req.method=='POST':
            steps=req.POST['steps']
            Cooking.objects.filter(pk=pid).update(steps=steps)
            data=Cooking.objects.get(pk=pid)
            return redirect('cooking',pid=data.dish.pk)
        else:
            data=Cooking.objects.get(pk=pid)
            return render(req,'editCook.html',{'data':data})
    else:
        return redirect(shop_login)
    
def deleteCook(req,pid):
    if 'user' in req.session:
        data=Cooking.objects.get(pk=pid)
        dId=data.dish.pk
        data.delete()
        return redirect('cooking',pid=dId)
    else:
        return redirect(shop_login)