from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('register',views.register),
    path('validate/<name>/<password>/<email>/<otp>',views.validate,name="validate"),
    path('logout',views.shp_logout),
    path('home',views.home),
    path('addRecipe',views.addRecipe),
    path('ingredients/<pid>',views.ingredients,name='ingredients'),
    path('cooking/<pid>',views.cooking,name='cooking'),

]