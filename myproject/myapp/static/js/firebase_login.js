import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import { initializeApp } from "firebase/app";

// Firebase конфіг (перенеси з твоєї конфігурації або імпортуй окремо)
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Коли натиснуто кнопку
document.getElementById("googleSignIn").addEventListener("click", () => {
  signInWithPopup(auth, provider)
    .then((result) => result.user.getIdToken())
    .then((idToken) => {
      // Надсилаємо токен на Django бекенд
      fetch("/api/protected/", {
        method: "GET",
        headers: {
          Authorization: idToken,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("Успішний вхід:", data);
          // можеш перенаправити: window.location.href = '/dashboard/';
        })
        .catch((err) => console.error("Помилка на бекенді:", err));
    })
    .catch((error) => {
      console.error("Помилка входу через Google:", error);
    });
});
