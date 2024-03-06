from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from accounts.models import customuser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import SignUpForm
from django import forms
from .models import Book,Notification
from .forms import BookForm
import firebase_admin
from firebase_admin import credentials, messaging
import os
import requests
import json
from guest_user.decorators import allow_guest_user
credentials_path = os.path.join(os.path.dirname(__file__), "credentials.json")


# Initialize Firebase Admin SDK with your credentials file
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred)
# Initialize Firebase Admin SDK
# firebase_cred = credentials.Certificate(credentials_path)
# firebase_admin.initialize_app(firebase_cred)
# from .models import Order
def home(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        return render(request,"home.html",{'notifications': notifications})
    else:
        return render(request,"home.html",{'notifications': []})

def menu(request):
    return render(request,"karte.html",{})

from django.db import transaction
def confirm(request):
    books = Book.objects.all()

# Use a transaction for atomicity
    with transaction.atomic():
        for book in books:
        # Check if confirmation value needs to be changed
            if book.confirmation != 'Ja':
                book.confirmation = 'Ja'
                user =book.user
                registration_tokens = [user.fcm_token]
                titel='Reservierungsbestätigung'
                message='Ihre Reservierung für ' +str(book.date)+ ' ist bestätigt'
                send_notification([user],registration_tokens, titel, message)
               

                book.save()
    return render(request, "home.html")

def account(request):
    if request.user.is_authenticated:
        return render(request, 'account.html', {'users': request.user})
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
    return redirect('login_user')


# def register_user(request):
#     # form = SignUpForm()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()

#             # Authenticate the new user
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             authenticated_user = authenticate(username=username, password=password)

#             # # Get the superuser
#             # superuser = customuser.objects.get(username='safarimac')
#             # super_fcm = superuser.fcm_token
#             # resgistration  = [super_fcm]
#             # send_notification(resgistration , 'New User' , 'New User')

#             superusers = customuser.objects.filter(is_superuser=True)
#             registration_tokens = [superuser.fcm_token for superuser in superusers]
#             send_notification(registration_tokens, 'New User', 'New User')

#             # Create a Notification object for the superuser
#             # Notification.objects.create(user=superuser, message=f"New user: {authenticated_user.username}")

#             messages.success(request, "New User!")
#             return redirect('home')
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")

#             messages.error(request, "Registration failed. Please correct the errors.")
#             return redirect('register_user')
#     else:
#         return render(request,'register_user.html',{'form':form})


from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')

        # Perform basic validation
        if not username or not password1 or password1 != password2:
            messages.error(request, "Registration failed. Please provide valid data.")
            return redirect('register_user')
        existing_users = customuser.objects.filter(username=username)

        if existing_users.exists():
            messages.error(request, "Registration failed. Please provide valid data.")
            return redirect('register_user')

          

        # Create user without using SignUpForm
        user = user = customuser.objects.create_user(username=username, password=password1, phone=phone,last_name=last_name)

        # Authenticate the new user
        authenticated_user = authenticate(username=username, password=password1)
        login(request, authenticated_user)
        # Notify superusers
        superusers = customuser.objects.filter(is_superuser=True)
        registration_tokens = [superuser.fcm_token for superuser in superusers]
        send_notification(superusers,registration_tokens, 'New User', 'New User')

        messages.success(request, "New User!")
        return redirect('home')
    else:
        return render(request, 'register_user.html', {})

# views.py

def orders_admin(request):
    if request.user.is_superuser:
        user_orders = Book.objects.filter(confirmation='Nein')
        return render(request, 'orders_admin.html', {'user_orders': user_orders})
    else:
        return redirect('home')


def user_orders(request):
    if request.user.is_authenticated:
        method = request.GET.get('method')
        if method == 'Show_Table':
            notification_id = request.GET.get('notification_id', None)
            notification = Notification.objects.filter(id=notification_id).first()
            if notification:
                notification.is_read = True
                notification.save()
        if request.user.is_superuser:
            return redirect('orders_admin')
        else:
            user_orders = Book.objects.filter(user=request.user)
            return render(request, 'user_orders.html', {'user_orders': user_orders,'method':method})
    else:
        return render(request, 'user_orders.html')
        # return render(request, 'user_orders.html', {'user_orders': 0})


def create_book(request):

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        decoration_value=request.POST.get('decoration')
        color = request.POST.get('color')
        comment = request.POST.get('comment')
        if decoration_value == 'on':
            decoration = True
        else:
            decoration = False
        if request.user.is_authenticated:
            user = request.user

            if not date or not time or not guests:
                messages.error(request, "Registrierungsfehler. Bitte geben Sie gültige Daten an.")
                return redirect('create_book')

            book = Book.objects.create(user=user, date=date,time=time,guests=guests,comment=comment,decoration=decoration,color=color)
            
            superusers = customuser.objects.filter(is_superuser=True)
            registration_tokens = [superuser.fcm_token for superuser in superusers]
            send_notification(superusers,registration_tokens, 'Neue Reservirung', f"{user.last_name} - {book.date} - {book.time} - {book.guests} pax")

            return redirect('user_orders') 
        else:
            phone = request.POST.get('phone')
            if not phone:
                username=request.POST.get('username')
                password=request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                else:
                    messages.error(request, "Falscher Login oder Passwort")
                    return redirect('create_book')
                book = Book.objects.create(user=user, date=date,time=time,guests=guests,comment=comment,decoration=decoration,color=color)
            
                superusers = customuser.objects.filter(is_superuser=True)
                registration_tokens = [superuser.fcm_token for superuser in superusers]
                send_notification(superusers,registration_tokens, 'Neue Reservirung', f"{user.last_name} - {book.date} - {book.time} - {book.guests} pax")
            else:
                guest_user_create_book(request)
                last_name=request.POST.get('last_name')
                request.user.name=last_name
                book = Book.objects.create(last_name=last_name,phone=phone, date=date,time=time,guests=guests,user=request.user,comment=comment,decoration=decoration,color=color)

                superusers = customuser.objects.filter(is_superuser=True)
                registration_tokens = [superuser.fcm_token for superuser in superusers]
                send_notification(superusers,registration_tokens, 'Neue Reservirung', f"{book.last_name} - {book.date} - {book.time} - {book.guests} pax")
                return redirect('user_orders') 


            

    else:
        pass
    return render(request, 'create_book.html') 

@allow_guest_user
def guest_user_create_book(request):
    print(request.user.username)

from .models import Notification
from .forms import NotificationForm

def show_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': notifications})

def create_notification(request):
    # superuser = customuser.objects.get(username='Sikophil')
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            Notification.objects.create(user=request.user, message=message)
            # Notification.objects.create(user=superuser, message=message)
            return redirect('show-notifications')
    else:
        form = NotificationForm()
    return render(request, 'create_notification.html', {'form': form})

from django.conf import settings
from django.http import JsonResponse

def manifest_view(request):
    manifest_path = os.path.join(settings.STATIC_ROOT, 'manifest.json')  # Assuming the manifest file is in your static folder
    with open(manifest_path) as manifest_file:
        manifest_data = json.load(manifest_file)
    return JsonResponse(manifest_data)

def icon_view(request):
    manifest_path = os.path.join(settings.STATIC_ROOT, 'icons/icon.png')  # Assuming the manifest file is in your static folder
    with open(manifest_path) as manifest_file:
        manifest_data = json.load(manifest_file)
    return JsonResponse(manifest_data)

###########
from django.http.request import HttpHeaders
from django.shortcuts import render

from django.http import HttpResponse
import requests
import json



def send_notification(users,registration_ids , message_title , message_desc):
    fcm_api = "AAAAS_Pnbmo:APA91bE2WuxV2c2L7sbnmzBd9JKaixg6yhgd5GXvETekUzbQltTApy1y7HfWbATx2D2HERXC1aRcAjrasnoBdd0Q7Xtx_s1CCS4Xw-6fWx8fIaiMYjG2_BIqZv1Tz01xkhDjK3n0cHVk"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}
    icon_url = os.path.join(settings.STATIC_URL,'icons/icon.png' )
    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "icon": icon_url
        }
    }
    for user in users:
        Notification.objects.create(user=user, title=message_title,message=message_desc)
    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())


def iconesave(request):
    image_path = os.path.join(settings.STATIC_ROOT, 'icons/icon.png')  # Adjust the path accordingly
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')

# def send(request):
#     # superuser = customuser.objects.get(username='Sikophil')
#     super_fcm = superuser.fcm_token
#     resgistration  = [super_fcm]
#     send_notification(resgistration , 'New Reservation' , 'New Reservation')
#     return HttpResponse("sent")




# def showFirebaseJS(request):
#     data='importScripts("https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js");' \
#          'importScripts("https://www.gstatic.com/firebasejs/10.8.0/firebase-messaging.js"); ' \
#          'var firebaseConfig = {' \
#          '        apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",' \
#          '        authDomain: "triglis-8c70f.firebaseapp.com",' \
#          '        projectId: "triglis-8c70f",' \
#          '        storageBucket: "triglis-8c70f.appspot.com",' \
#          '        messagingSenderId: "326214577770",' \
#          '        appId: "1:326214577770:web:cb91775ceef9401eab2413",' \
#          '        measurementId: "G-WTXNXDVTZ7"' \
#          ' };' \
#          'firebase.initializeApp(firebaseConfig);' \
#          'const messaging=firebase.messaging();' \
#          'messaging.setBackgroundMessageHandler(function (payload) {' \
#          '    console.log(payload);' \
#          '    const notification = payload.data;' \
#          '    const notificationOption={' \
#          '        body:notification.body,' \
#          '    };' \
#          '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
#          '});'

#     return HttpResponse(data,content_type="text/javascript")


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt  # Make sure to add csrf_exempt decorator if you don't want to deal with CSRF tokens in this example
# def save_firebase_token(request):
#     if request.method == 'POST':
#         # Assuming you send the token as a JSON object in the request body
#         token = request.POST.get('token')

#         # Save the token in your database or perform any other desired actions
#         # Example:
#         # YourModel.objects.create(firebase_token=token)

#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def update_fcm_token(request):
    if request.method == 'POST':
        current_token = request.POST.get('currentToken')
        request.user.fcm_token = current_token
        request.user.save()
        return JsonResponse({'message': 'Token updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    



from firebase_admin import messaging

def send_push_notification(user_fcm_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=user_fcm_token,
    )

    # Send the message
    response = messaging.send(message)

    print('Successfully sent message:', response)