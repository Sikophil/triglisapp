from . import views
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
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
    # path('send/' , views.send),
    # path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    re_path('firebase-messaging-sw.js', serve, {'document_root': settings.STATIC_ROOT, 'path': 'js/firebase-messaging-sw.js'}),
    path('update_fcm_token/', views.update_fcm_token, name='update_fcm_token'),
] 