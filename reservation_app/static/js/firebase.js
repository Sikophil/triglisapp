
import { initializeApp } from "firebase/app";
import { getMessaging, getToken } from "firebase/messaging";

const firebaseConfig = {
  apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",
  authDomain: "triglis-8c70f.firebaseapp.com",
  projectId: "triglis-8c70f",
  storageBucket: "triglis-8c70f.appspot.com",
  messagingSenderId: "326214577770",
  appId: "1:326214577770:web:cb91775ceef9401eab2413",
  measurementId: "G-WTXNXDVTZ7"
};


// Initialize Firebase
const app = initializeApp(firebaseConfig);


// Initialize Firebase Cloud Messaging and get a reference to the service
const messaging = getMessaging(app);
// Add the public key generated from the console here.
getToken(messaging, {vapidKey: "BK8quVdKKHUockQYSVKEkeu2FheWYzBH9wcHYB7Ko-IbNYQsJoCvE9A7FsooT9c5pTfSVs7fSGzT8jmfukErGXE"});