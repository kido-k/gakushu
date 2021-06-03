import firebase from 'firebase'

// .env に設定した値を取得してる
const firebaseConfig = {
  apiKey: process.env.API_KEY,
  authDomain: process.env.AUTH_DOMAIN,
  databaseURL: process.env.DATABASE_URL,
  projectId: process.env.PROJECT_ID,
  storageBucket: process.env.STORAGE_BUCKET,
  messagingSenderId: process.env.MESSAGING_SEND_ID,
  appID: process.env.APP_ID,
  measurementId: process.env.MEASUREMENT_ID,
}

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig)
}

export default (_, inject) => {
  inject('firebase', firebase)
}
