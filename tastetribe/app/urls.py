from django.urls import path
from . import views

urlpatterns=[
    path('',views.shop_login),
    path('register',views.register),
    path('validate/<name>/<password>/<email>/<otp>',views.validate,name="validate"),
    path('logout',views.shp_logout),
    path('home',views.home),
    path('profile',views.profile),
    path('addRecipe',views.addRecipe),
    path('ingredients/<pid>',views.ingredients,name='ingredients'),
    path('cooking/<pid>',views.cooking,name='cooking'),
    path('edit/<pid>',views.edit,name='edit'),
    path('editIngr/<pid>',views.editIngr,name='editIngr'),
    path('deleteIngr/<pid>',views.deleteIngr,name='deleteIngr'),
    path('editCook/<pid>',views.editCook,name='editCook'),
    path('deleteCook/<pid>',views.deleteCook,name='deleteCook'),
    path('addLike/<pid>',views.addLike),
    path('removeLike/<pid>',views.removeLike),
    path('viewUser/<pid>',views.viewUser),

]