// firebase.js
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",
  authDomain: "triglis-8c70f.firebaseapp.com",
  projectId: "triglis-8c70f",
  storageBucket: "triglis-8c70f.appspot.com",
  messagingSenderId: "326214577770",
  appId: "1:326214577770:web:6641bab6a9ce2882ab2413",
  measurementId: "G-LN4GYPHG6P"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
// const db = getFirestore(app);
const messaging = getMessaging(app);
getToken(messaging, { vapidKey: 'BK8quVdKKHUockQYSVKEkeu2FheWYzBH9wcHYB7Ko-IbNYQsJoCvE9A7FsooT9c5pTfSVs7fSGzT8jmfukErGXE' }).then((currentToken) => {
if (currentToken) {
  console.log('THIS');
  console.log(currentToken);
} else {
  // Show permission request UI
  console.log('No registration token available. Request permission to generate one.');
  // ...
}
}).catch((err) => {
console.log('An error occurred while retrieving token. ', err);
// ...
});

// <script type="module">
// // Import the functions you need from the SDKs you need
//   import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
//   import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics.js";
//   // TODO: Add SDKs for Firebase products that you want to use
//   // https://firebase.google.com/docs/web/setup#available-libraries

//   // Your web app's Firebase configuration
//   // For Firebase JS SDK v7.20.0 and later, measurementId is optional
//   const firebaseConfig = {
//     apiKey: "AIzaSyCtnbzPNKXXP0ecFOdX6HnH0WAZdSTTEXo",
//     authDomain: "triglis-8c70f.firebaseapp.com",
//     projectId: "triglis-8c70f",
//     storageBucket: "triglis-8c70f.appspot.com",
//     messagingSenderId: "326214577770",
//     appId: "1:326214577770:web:cb91775ceef9401eab2413",
//     measurementId: "G-WTXNXDVTZ7"
//   };

//   // Initialize Firebase
//   const app = initializeApp(firebaseConfig);
//   const analytics = getAnalytics(app);
// </script>