const { initializeApp, cert } = require('firebase-admin/app');
const { getFirestore } = require('firebase-admin/firestore');
const serviceAccount = require('./firebaseKey.json');
const dotenv = require('dotenv');
dotenv.config();

const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: 'photo-exam.firebaseapp.com',
  projectId: 'photo-exam',
  storageBucket: 'photo-exam.appspot.com',
  messagingSenderId: '609493449218',
  appId: '1:609493449218:web:c13bf48330869fb23e051b',
};

initializeApp({
  credential: cert(serviceAccount),
});

const db = getFirestore();
const usersRef = db.collection('users');
const collectionsRef = db.collection('files');

module.exports = { db, usersRef, collectionsRef };
