import pyrebase

# Firebase configuration
firebase_config = {
    'apiKey': "AIzaSyDF6K3fW1W0lK76WHLyS_3vCWkrMooXSJc",
  'authDomain': "recomendation-system-985c3.firebaseapp.com",
  'projectId': "recomendation-system-985c3",
  'storageBucket': "recomendation-system-985c3.appspot.com",
  'messagingSenderId': "330733729225",
  'appId': "1:330733729225:web:0943a3d0eca74f29272418",
  'measurementId': "G-LLX8649PSN",
    'databaseURL': "https://recomendation-system-985c3.firebaseio.com"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()


