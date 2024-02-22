// firebase.js
// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
var firebaseConfig = {
  apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",
  authDomain: "triglis-8c70f.firebaseapp.com",
  projectId: "triglis-8c70f",
  storageBucket: "triglis-8c70f.appspot.com",
  messagingSenderId: "326214577770",
  appId: "1:326214577770:web:cb91775ceef9401eab2413",
  measurementId: "G-WTXNXDVTZ7"
};

// Initialize Firebase
var app = firebase.initializeApp(firebaseConfig);

// Specify the correct path to firebase-messaging-sw.js within the static folder

// Retrieve the FCM token
firebase.messaging().getToken({ vapidKey: "YOUR_VAPID_KEY" })
  .then((currentToken) => {
    if (currentToken) {
      console.log("FCM Token:", currentToken);
      // You can use the token as needed
    } else {
      console.log("No registration token available.");
    }
  })
  .catch((err) => {
    console.error("Error getting FCM token:", err);
  });
