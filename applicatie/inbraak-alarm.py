import pyrebase

config = {
  "apiKey": "AIzaSyDse4S8imxqiaDRELr58a8P45r7G5Af2go",
  "authDomain": "miniproject-computersystems.firebaseapp.com",
  "databaseURL": "https://miniproject-computersystems.firebaseio.com",
  "storageBucket": "miniproject-computersystems.appspot.com"
}

firebase = pyrebase.initialize_app(config)