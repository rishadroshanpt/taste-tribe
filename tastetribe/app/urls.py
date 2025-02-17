from django.urls import path
from . import views

urlpatterns=[
    path('shop_login',views.shop_login,name='shop_login'),
    path('validate',views.validate,name="validate"),
    path('logout',views.shp_logout),
    path('',views.home),


    # -----------------------------admin----------------------------
    path('adminHome',views.adminHome),
    path('reports',views.reports),
    path('viewUserAdmin/<pid>',views.viewUserAdmin,name='viewUserAdmin'),
    path('adminDish/<pid>',views.adminDish,name='adminDish'),



    # -----------------------------user-----------------------------


    path('userHome',views.userHome),
    path('explore',views.explore),
    path('search_dishes/', views.search_dishes, name='search_dishes'),
    path('profile',views.profile),
    path('addRecipe',views.addRecipe),
    path('delete/<pid>',views.delete),
    path('ingredients/<pid>',views.ingredients,name='ingredients'),
    path('cooking/<pid>',views.cooking,name='cooking'),
    path('edit/<pid>',views.edit,name='edit'),
    path('editIngr/<pid>',views.editIngr,name='editIngr'),
    path('deleteIngr/<pid>',views.deleteIngr,name='deleteIngr'),
    path('editCook/<pid>',views.editCook,name='editCook'),
    path('deleteCook/<pid>',views.deleteCook,name='deleteCook'),
    path('like/<pid>/', views.like, name='like'),
    path('addLike/<pid>',views.addLike,name='addLike'),
    path('removeLike/<pid>',views.removeLike),
    path('viewUser/<pid>',views.viewUser,name='viewUser'),
    path('feedbacks/<pid>',views.feedbacks,name='feedbacks'),
    path('follow/<uid>', views.follow_user, name='follow_user'),
    path('unfollow/<uid>', views.unfollow_user, name='unfollow_user'),
    path('save/<pid>',views.save),
    path('unsave/<pid>',views.unsave),
    path('report/<pid>',views.report),
    path('saved',views.saved),
    path('notifications',views.notifications_view),
    path('editProfile',views.editProfile),


]