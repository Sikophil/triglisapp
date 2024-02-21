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
credentials_path = os.path.join(os.path.dirname(__file__), "credentials.json")

# Initialize Firebase Admin SDK
firebase_cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(firebase_cred)
# from .models import Order
def home(request):
    return render(request,"home.html",{})
 
# def book(request,pk):
#     book = Book.objects.get(id=pk)
#     return render(request,"book.html",{'book':book})

def menu(request):
    return render(request,"menu.html",{})

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
            message = messaging.Message(
                data={
                    "title": "New User Created!",
                    "body": f"New user: {authenticated_user.username}",
                },
                token=superuser.fcm_token,  # Replace with the superuser's FCM token field
            )
            messaging.send(message)

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