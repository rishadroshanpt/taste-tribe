from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings   
import math,random
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow, Like, Notification
from django.http import JsonResponse
from django.db.models import Q 


# Create your views here.
def shop_login(req):
    if 'admin' in req.session:
        return redirect(adminHome)
    if 'user' in req.session:
        return redirect(userHome)
    if req.method == 'POST':
        if 'uname' in req.POST and 'passwd' in req.POST:
            uname = req.POST['uname']
            password = req.POST['passwd']
            data = authenticate(username=uname, password=password)
            if data :
                if data.is_superuser:
                    req.session['admin']=uname   #create session
                    return redirect(adminHome)
                else:
                    req.session['user']=uname   #create session
                    return redirect(userHome)
            else:
                messages.warning(req,'Invalid username or password.')
                return redirect(shop_login)
        elif 'name' in req.POST and 'email' in req.POST and 'passwd' in req.POST:
            # This is for sign-up
            name = req.POST['name']
            email = req.POST['email']
            password = req.POST['passwd']
            otp=OTP(req)
            req.session['name'] = name
            req.session['email'] = email
            req.session['password'] = password
            req.session['otp'] = otp
            if User.objects.filter(email=email).exists():
                messages.error(req, "Email is already in use.")
                return redirect(shop_login)
            else:
                send_mail('Your registration OTP ,',f"OTP for registration is {otp}", settings.EMAIL_HOST_USER, [email])
                messages.success(req, "Registration successful. Please check your email for OTP.")
                return redirect("validate")    
        else:
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


def validate(req):
    if req.method=='POST':
        uotp=req.POST['uotp']
        name = req.session.get('name')
        email = req.session.get('email')
        password = req.session.get('password')
        otp = req.session.get('otp')
        if uotp==otp:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            messages.success(req, "OTP verified successfully. You can now log in.")
            return redirect(shop_login)
        else:
            messages.error(req, "Invalid OTP. Please try again.")
            return redirect("validate")
    else:
        return render(req,'validate.html')




# -----------------admin-----------------------------

def adminHome(req):
    if 'admin' in req.session:
        user=User.objects.get(username=req.session['admin'])
        dish=Dish.objects.all()[: : -1]
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        save=Saved.objects.all()
        liked_dishes = [like.dish.pk for like in like if like.user.pk == user.pk]
        saved_dishes = [save.dish.pk for save in save if save.user.pk == user.pk]
        unread_count = Notification.objects.filter(user=user, read=False).count()
        return render(req,'admin/home.html',{'dish':dish,'ingr':ingr,'cook':cook,'like':like,'liked_dishes':liked_dishes,'saved_dishes':saved_dishes,'unread_count':unread_count})
    else:
        return redirect(shop_login)
    
def adminDish(req,pid):
    if 'admin' in req.session:
        # user=User.objects.get(username=req.session['admin'])
        dish=Dish.objects.get(pk=pid)
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        save=Saved.objects.all()
        # liked_dishes = [like.dish.pk for like in like if like.user.pk == user.pk]
        # saved_dishes = [save.dish.pk for save in save if save.user.pk == user.pk]
        return render(req,'admin/dish.html',{'data':dish,'ingr':ingr,'cook':cook,'like':like})
    else:
        return redirect(shop_login)

def reports(req):
    if 'admin' in req.session:
        # user=User.objects.get(username=req.session['admin'])
        data=Report.objects.all()[: : -1]
        return render(req,'admin/reports.html',{'data':data})
    else:
        return redirect(shop_login)

    
def viewUserAdmin(req,pid):
    if 'admin' in req.session:
        user1=User.objects.get(username=req.session['admin'])
        user=User.objects.get(pk=pid)
        dish=Dish.objects.filter(user=user)
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        save=Saved.objects.all()
        liked_dishes = [like.dish.pk for like in like if like.user.pk == user1.pk]
        saved_dishes = [save.dish.pk for save in save if save.user.pk == user1.pk]
        post=dish.count()
        followers = (user.followers.all()).count()
        following = (user.following.all()).count()
        unread_count = Notification.objects.filter(user=user1, read=False).count()
        is_following =  Follow.objects.filter(follower=user1, following=user).exists()
        return render(req,'admin/viewUser.html',{'dish':dish,'ingr':ingr,'cook':cook,'liked_dishes':liked_dishes,'is_following':is_following,'user':user,'user1':user1,'post':post,'followers':followers,'following':following,'saved_dishes':saved_dishes,'unread_count':unread_count})
    else:
        return redirect(shop_login)

def removeReport(req,pid):
    data=Report.objects.get(dish=pid)
    # print(data)
    data.delete()
    return redirect(reports)


# -------------------user----------------------------

def home(req):
    if 'user' in req.session:
        return redirect(userHome)
    else:
        dish=Dish.objects.all()[: : -1]
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        return render(req,'home.html',{'dish':dish,'ingr':ingr,'cook':cook})


def userHome(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        dish = Dish.objects.filter(user__in=following_users).union(Dish.objects.filter(user=user))[: : -1]
        # dish=Dish.objects.all()[: : -1]
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        save=Saved.objects.all()
        liked_dishes = [like.dish.pk for like in like if like.user.pk == user.pk]
        saved_dishes = [save.dish.pk for save in save if save.user.pk == user.pk]
        unread_count = Notification.objects.filter(user=user, read=False).count()
        return render(req,'home.html',{'dish':dish,'ingr':ingr,'cook':cook,'like':like,'liked_dishes':liked_dishes,'saved_dishes':saved_dishes,'unread_count':unread_count})
    else:
        return redirect(shop_login)
    
def explore(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        dish=Dish.objects.all()[: : -1]
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        save=Saved.objects.all()
        liked_dishes = [like.dish.pk for like in like if like.user.pk == user.pk]
        saved_dishes = [save.dish.pk for save in save if save.user.pk == user.pk]
        unread_count = Notification.objects.filter(user=user, read=False).count()
        return render(req,'explore.html',{'dish':dish,'ingr':ingr,'cook':cook,'like':like,'liked_dishes':liked_dishes,'saved_dishes':saved_dishes,'unread_count':unread_count})
    else:
        return redirect(shop_login)
    
def result(req):
    return render(req,'result.html')

def search_dishes(req):
    query = req.GET.get('q', '')  # Get the search query from the request
  # Assuming you are using the logged-in user
    dishes=[]
    users=[]
    if query:
        # Search across dish name, cuisine, and user (case-insensitive search)
        dishes = Dish.objects.filter(Q(name__icontains=query) | Q(cuisine__icontains=query))
        users = User.objects.filter(Q(first_name__icontains=query))
    dishes_data = []
    for dish in dishes:
        dishes_data.append({
            'id': dish.id,
            'name': dish.name,
            'cuisine': dish.cuisine,
            'img_url': dish.img.url if dish.img else '',
        })

    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'first_name': user.first_name,
            'profile_img': user.bio.img.url if user.bio and user.bio.img else '',  # Adjust based on your model
        })
    print(dishes_data)
    # Return the data as JSON
    return JsonResponse({
        'dishes': dishes_data,
        'users': users_data,
    })


    # Return the HTML fragment with the search results


    
def profile(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        dish=Dish.objects.filter(user=user)
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        save=Saved.objects.all()
        liked_dishes = [like.dish.pk for like in like if like.user.pk == user.pk]
        saved_dishes = [save.dish.pk for save in save if save.user.pk == user.pk]
        post=dish.count()
        followers = (user.followers.all()).count()
        following = (user.following.all()).count()
        unread_count = Notification.objects.filter(user=user, read=False).count()
        return render(req,'profile.html',{'dish':dish,'ingr':ingr,'cook':cook,'liked_dishes':liked_dishes,'user':user,'post':post,'followers':followers,'following':following,'saved_dishes':saved_dishes,'unread_count':unread_count})
    else:
        return redirect(shop_login)
    
def viewUser(req,pid):
    if 'user' in req.session:
        user1=User.objects.get(username=req.session['user'])
        user=User.objects.get(pk=pid)
        dish=Dish.objects.filter(user=user)
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        save=Saved.objects.all()
        liked_dishes = [like.dish.pk for like in like if like.user.pk == user1.pk]
        saved_dishes = [save.dish.pk for save in save if save.user.pk == user1.pk]
        post=dish.count()
        followers = (user.followers.all()).count()
        following = (user.following.all()).count()
        unread_count = Notification.objects.filter(user=user1, read=False).count()
        is_following =  Follow.objects.filter(follower=user1, following=user).exists()
        if user1 == user :
            return redirect(profile)
        else:
            return render(req,'viewUser.html',{'dish':dish,'ingr':ingr,'cook':cook,'liked_dishes':liked_dishes,'is_following':is_following,'user':user,'user1':user1,'post':post,'followers':followers,'following':following,'saved_dishes':saved_dishes,'unread_count':unread_count})
    else:
        return redirect(shop_login)
    
def dish(req,pid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        dish=Dish.objects.get(pk=pid)
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        save=Saved.objects.all()
        liked_dishes = [like.dish.pk for like in like if like.user.pk == user.pk]
        saved_dishes = [save.dish.pk for save in save if save.user.pk == user.pk]
        unread_count = Notification.objects.filter(user=user, read=False).count()
        return render(req,'dish.html',{'data':dish,'ingr':ingr,'cook':cook,'like':like,'liked_dishes':liked_dishes,'saved_dishes':saved_dishes,'unread_count':unread_count})
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
            data=Dish.objects.create(user=user,name=name,img=img,cuisine=cuisine,prep=prep,cook=cook,likes=0)
            data.save()
            pk=data.pk
            return redirect("ingredients",pid=pk)
        else:
            unread_count = Notification.objects.filter(user=User.objects.get(username=req.session['user']), read=False).count()
            return render(req,'addRecipe.html',{'unread_count':unread_count})
    else:
        return redirect(shop_login)
    
def delete(req,pid):
    if 'user' in req.session:
        data=Dish.objects.get(pk=pid)
        data.delete()
        return redirect(profile)
    if 'admin' in req.session:
        data=Dish.objects.get(pk=pid)
        data.delete()
        return redirect(reports)
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
            unread_count = Notification.objects.filter(user=User.objects.get(username=req.session['user']), read=False).count()
            return render(req,'ingredients.html',{'data':data,'dish':dish,'unread_count':unread_count})
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
            unread_count = Notification.objects.filter(user=User.objects.get(username=req.session['user']), read=False).count()
            return render(req,'cooking.html',{'data':data,'dish':dish,'unread_count':unread_count})
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
            unread_count = Notification.objects.filter(user=User.objects.get(username=req.session['user']), read=False).count()
            return render(req,'edit.html',{'data':data,'unread_count':unread_count})
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
            unread_count = Notification.objects.filter(user=User.objects.get(username=req.session['user']), read=False).count()
            return render(req,'editIngr.html',{'data':data,'unread_count':unread_count})
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
            unread_count = Notification.objects.filter(user=User.objects.get(username=req.session['user']), read=False).count()
            return render(req,'editCook.html',{'data':data,'unread_count':unread_count})
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
    
def like(req,pid):
    if 'user' in req.session:
        dish = Dish.objects.get(pk=pid)
        user = User.objects.get(username=req.session['user'])
    # Check if the user has already liked the dish
        existing_like = Like.objects.filter(user=user, dish=dish).first()
    
        if existing_like:
            # Unlike the dish
            existing_like.delete()
            dish.likes -= 1
            dish.save()
            liked = False
        else:
            # Like the dish
            Like.objects.create(user=user, dish=dish)
            dish.likes += 1
            dish.save()
            liked = True

        return JsonResponse({
            'liked': liked,
            'like_count': dish.likes
        })
    else:
        return redirect(shop_login)
    
def addLike(req,pid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        dish=Dish.objects.get(pk=pid)
        dish.likes+=1
        dish.save()
        data=Like.objects.create(dish=dish,user=user)
        data.save()
        # return redirect(home)
        return redirect(req.META.get('HTTP_REFERER'))
    else:
        return redirect(shop_login)

def removeLike(req,pid):
    if 'user' in req.session:
        data=Dish.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        data.likes-=1
        data.save()
        data=Like.objects.get(dish=pid,user=user)
        data.delete()
        # return redirect(home)
        return redirect(req.META.get('HTTP_REFERER'))
    else:
        return redirect(shop_login)
    
def report(req,pid):
    if 'user' in req.session:
        dish=Dish.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        data=Report.objects.create(dish=dish,user=user)
        data.save()
        return redirect(req.META.get('HTTP_REFERER'))
    else:
        return redirect(shop_login)

def feedbacks(req,pid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        dish=Dish.objects.get(pk=pid)
        if req.method=='POST':
            rate=req.POST['rating']
            data=Ratings.objects.create(user=user,dish=dish,ratings=rate)
            data.save()
            return redirect('feedbacks',pid=pid)
        else:
            data=Ratings.objects.filter(dish=pid)
            ingr=Ingredients.objects.filter(dish=pid)
            cook=Cooking.objects.filter(dish=pid)
            unread_count = Notification.objects.filter(user=User.objects.get(username=req.session['user']), read=False).count()
            return render(req,'ratings.html',{'data':data,'dish':dish,'ingr':ingr,'cook':cook,'unread_count':unread_count})
    else:
        return redirect(shop_login)
    
def follow_user(req, uid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        user_to_follow = User.objects.get(pk=uid)
        if user != user_to_follow:  # A user cannot follow themselves
            Follow.objects.create(follower=user, following=user_to_follow)
        return redirect('viewUser', pid=uid)
    else:
        return redirect(shop_login)

def unfollow_user(req, uid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        user_to_unfollow = User.objects.get(pk=uid)
        if user != user_to_unfollow:
            Follow.objects.filter(follower=user, following=user_to_unfollow).delete()
        return redirect('viewUser', pid=uid)
    else:
        return redirect(shop_login)

def save(req,pid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        dish=Dish.objects.get(pk=pid)
        data=Saved.objects.create(dish=dish,user=user)
        data.save()
        return redirect(req.META.get('HTTP_REFERER'))
    else:
        return redirect(shop_login) 
    
def unsave(req,pid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        dish=Dish.objects.get(pk=pid)
        data=Saved.objects.get(dish=dish,user=user)
        data.delete()
        return redirect(req.META.get('HTTP_REFERER'))
    else:
        return redirect(shop_login) 

def saved(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Saved.objects.filter(user=user)
        ingr=Ingredients.objects.all()
        cook=Cooking.objects.all()
        like=Like.objects.all()
        unread_count = Notification.objects.filter(user=User.objects.get(username=req.session['user']), read=False).count()
        liked_dishes = [like.dish.pk for like in like if like.user.pk == user.pk]
        return render(req,'saved.html',{'data':data,'ingr':ingr,'cook':cook,'liked_dishes':liked_dishes,'unread_count':unread_count})
    else:
        return redirect(shop_login)
    


def notifications_view(req):
    user=User.objects.get(username=req.session['user'])
    notifications = Notification.objects.filter(user=user)
    notifications.filter(read=False).update(read=True)
    return render(req, 'notifications.html', {'notifications': notifications})

def editProfile(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        if req.method=='POST':
            img=req.FILES.get('img')
            bio=req.POST['bio']
            name=req.POST['name']
            if img:
                User.objects.filter(pk=user.pk).update(first_name=name)
                Bio.objects.filter(user=user).update(bio=bio)
                data=Bio.objects.get(user=user)
                url=data.img.url
                og_path=url.split('/')[-1]
                print(og_path)
                if og_path != 'profile.jpg':
                    os.remove('media/profile_pics/'+og_path)
                data.img=img
                data.save()
            else:
                User.objects.filter(pk=user.pk).update(first_name=name)
                Bio.objects.filter(user=user).update(bio=bio)
            return redirect(profile)
        else:
            return render(req,'editProfile.html',{'user':user})
    else:
        return redirect(shop_login)