
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

var firebaseConfig = {   
    apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",      
    authDomain: "triglis-8c70f.firebaseapp.com",     
    projectId: "triglis-8c70f",     
    storageBucket: "triglis-8c70f.appspot.com",        
    messagingSenderId: "326214577770",        
    appId: "1:326214577770:web:cb91775ceef9401eab2413",        
    measurementId: "G-WTXNXDVTZ7"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
    console.log(payload);
    const notification = payload.data;
    const notificationOption = {
        body: notification.body,
    };
    // Use 'self' to show the notification
    return self.registration.showNotification(payload.notification.title, notificationOption);
});
// import { initializeApp } from 'firebase/app';
// import { getMessaging, onBackgroundMessage } from 'firebase/messaging';

// // Import the 'self' object
// import { register } from 'service-worker';

// const firebaseConfig = {   
//     apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",      
//     authDomain: "triglis-8c70f.firebaseapp.com",     
//     projectId: "triglis-8c70f",     
//     storageBucket: "triglis-8c70f.appspot.com",        
//     messagingSenderId: "326214577770",        
//     appId: "1:326214577770:web:cb91775ceef9401eab2413",        
//     measurementId: "G-WTXNXDVTZ7"
// };

// // Initialize Firebase
// const app = initializeApp(firebaseConfig);

// // Retrieve Firebase Messaging instance
// const messaging = getMessaging(app);

// // Set up background message handler
// onBackgroundMessage(messaging, (payload) => {
//     console.log('Received background message:', payload);

//     // Customize the notification payload and show the notification
//     const notificationTitle = 'Background Message Title';
//     const notificationOptions = {
//         body: payload.data.body,
//     };

//     // Use the 'self' object to show the notification
//     self.registration.showNotification(notificationTitle, notificationOptions);
// });

