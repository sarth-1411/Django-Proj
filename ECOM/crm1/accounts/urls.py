from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('product/',views.product,name="products"),
    path('login/',views.Login,name="login"),
    path('logout/',views.Logout,name="logout"),
    path('register/',views.Register,name="register"),
    path('user/', views.userPage, name="user-page"),
    path('account/',views.accountsSetting,name="account"),
    path('contact/<str:pk_text>/',views.contact,name="customer"),
    path('create_order/<str:pk>',views.createOrder,name="create_order"),
    path('update_order/<str:pk>',views.updateOrder,name="update_order"),
    path('delete_order/<str:pk>',views.deleteOrder,name="delete_order"),
]
   

