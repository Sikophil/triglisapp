from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from .models import Book
from .forms import OrderForm,BookForm
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
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username,password=password)
            superuser = User.objects.get(username='Sikophil')
            Notification.objects.create(user=superuser, message='NewUser!')
            messages.success(request,("New User!"))
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
    superuser = User.objects.get(username='Sikophil')
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