// firebase.js

import { initializeApp } from 'firebase/app';
// import { getFirestore, collection, getDocs } from 'firebase/firestore/lite';
import { getMessaging, getToken } from "firebase/messaging";
// TODO: Replace the following with your app's Firebase project configuration
const firebaseConfig = {
    apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",
    authDomain: "triglis-8c70f.firebaseapp.com",
    projectId: "triglis-8c70f",
    storageBucket: "triglis-8c70f.appspot.com",
    messagingSenderId: "326214577770",
    appId: "1:326214577770:web:cb91775ceef9401eab2413",
    measurementId: "G-WTXNXDVTZ7"
  };

const app = initializeApp(firebaseConfig);
// const db = getFirestore(app);
const messaging = getMessaging(app);
getToken(messaging, { vapidKey: 'BK8quVdKKHUockQYSVKEkeu2FheWYzBH9wcHYB7Ko-IbNYQsJoCvE9A7FsooT9c5pTfSVs7fSGzT8jmfukErGXE' }).then((currentToken) => {
if (currentToken) {
  // Send the token to your server and update the UI if necessary
  // ...
} else {
  // Show permission request UI
  console.log('No registration token available. Request permission to generate one.');
  // ...
}
}).catch((err) => {
console.log('An error occurred while retrieving token. ', err);
// ...
});
