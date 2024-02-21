from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('menu/', views.menu, name='menu'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('register_user/',views.register_user,name='register_user'),
    path('user/orders/', views.user_orders, name='user_orders'),
    path('create/', views.create_book, name='create_book'),
    path('notifications/', views.show_notifications, name='show-notifications'),
    path('create_notification/', views.create_notification, name='create-notification'),
] 