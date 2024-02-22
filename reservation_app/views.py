from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from accounts.models import customuser

from .forms import SignUpForm
from django import forms
from .models import Book
from .forms import OrderForm,BookForm
import firebase_admin
from firebase_admin import credentials, messaging
import os
import requests
import json
# credentials_path = os.path.join(os.path.dirname(__file__), "credentials.json")

# Initialize Firebase Admin SDK
# firebase_cred = credentials.Certificate(credentials_path)
# firebase_admin.initialize_app(firebase_cred)
# from .models import Order
def home(request):
    return render(request,"home.html",{})
 

def menu(request):
    if request.user.is_authenticated:
        return render(request, 'menu.html', {'users': request.user})
    else:
        # Handle the case when the user is not authenticated, e.g., redirect to login page
        return render(request, 'login.html')
    

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request,("Error"))
            return redirect('login_user')
        
        
    else:
        pass

    
    return render(request,"login.html",{})

def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Authenticate the new user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            authenticated_user = authenticate(username=username, password=password)

            # Get the superuser
            superuser = customuser.objects.get(username='Sikophil')

            # Send push notification
            # message = messaging.Message(
            #     data={
            #         "title": "New User Created!",
            #         "body": f"New user: {authenticated_user.username}",
            #     },
            #     token=superuser.fcm_token,  # Replace with the superuser's FCM token field
            # )
            # messaging.send(message)

            # Create a Notification object for the superuser
            Notification.objects.create(user=superuser, message=f"New user: {authenticated_user.username}")

            messages.success(request, "New User!")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            messages.error(request, "Registration failed. Please correct the errors.")
            return redirect('register_user')
    else:
        return render(request,'register_user.html',{'form':form})

# views.py

def user_orders(request):
    if request.user.is_authenticated:
        user_orders = Book.objects.filter(user=request.user)
        return render(request, 'user_orders.html', {'user_orders': user_orders})
    else:
        # Handle the case when the user is not authenticated, e.g., redirect to login page
        return render(request, 'login.html')


def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.user = request.user
            new_book.save()
            return redirect('home')  # Redirect to a page displaying a list of books
    else:
        form = BookForm()

    return render(request, 'create_book.html', {'form': form})

from .models import Notification
from .forms import NotificationForm

def show_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': notifications})

def create_notification(request):
    superuser = customuser.objects.get(username='Sikophil')
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            Notification.objects.create(user=request.user, message=message)
            Notification.objects.create(user=superuser, message=message)
            return redirect('show-notifications')
    else:
        form = NotificationForm()
    return render(request, 'create_notification.html', {'form': form})





###########
from django.http.request import HttpHeaders
from django.shortcuts import render

from django.http import HttpResponse
import requests
import json



def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAAS_Pnbmo:APA91bE2WuxV2c2L7sbnmzBd9JKaixg6yhgd5GXvETekUzbQltTApy1y7HfWbATx2D2HERXC1aRcAjrasnoBdd0Q7Xtx_s1CCS4Xw-6fWx8fIaiMYjG2_BIqZv1Tz01xkhDjK3n0cHVk"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())





def index(request):
    return render(request , 'index.html')

def send(request):
    resgistration  = ['fvgbyCymRY-14C6V6UNRwu:APA91bHRemdcdwEUwzxjT7uVPmt7LbIzPUIVhpWoH6TlJMXkJ7YZI4oqC43AKl8kRJal5MZzV_gxOIGUaC_ceXYvJEILn9WtX3QDdvU9eZ9kmj6FvXzE8dJUNmV6j3vw40DQDSF-doxW'
    ]
    send_notification(resgistration , 'Code Keen added a new video' , 'Code Keen new video alert')
    return HttpResponse("sent")




def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",' \
         '        authDomain: "triglis-8c70f.firebaseapp.com",' \
         '        projectId: "triglis-8c70f",' \
         '        storageBucket: "triglis-8c70f.appspot.com",' \
         '        messagingSenderId: "326214577770",' \
         '        appId: "1:326214577770:web:cb91775ceef9401eab2413",' \
         '        measurementId: "G-WTXNXDVTZ7"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")