importScripts("https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/10.8.0/firebase-messaging.js");
var firebaseConfig = {   
    apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",      
    authDomain: "triglis-8c70f.firebaseapp.com",     
    projectId: "triglis-8c70f",     
    storageBucket: "triglis-8c70f.appspot.com",        
    messagingSenderId: "326214577770",        
    appId: "1:326214577770:web:cb91775ceef9401eab2413",        
    measurementId: "G-WTXNXDVTZ7" };
firebase.initializeApp(firebaseConfig);
const messaging=firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {    console.log(payload);
const notification = payload.data;    
const notificationOption={        body:notification.body,    };    
return self.registration.showNotification(payload.notification.title,notificationOption);});