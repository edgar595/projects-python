import pyrebase

config = {
  'apiKey': "AIzaSyBoF9TYrU6Vvh9xxkpP7Omn_e1kYsDSVgI",
  'authDomain': "first-aa0d4.firebaseapp.com",
  'databaseURL': "https://first-aa0d4-default-rtdb.firebaseio.com",
  'projectId': "first-aa0d4",
  'storageBucket': "first-aa0d4.appspot.com",
  'messagingSenderId': "98927499335",
  'appId': "1:98927499335:web:642ed7333d04ed88477962"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

#register
email = 'test@gmail.com'
password = '123456'


#user = auth.create_user_with_email_and_password(email, password)
#print(user)

user = auth.sign_in_with_email_and_password(email, password)

#info = auth.get_account_info(user['idToken'])
#print(info)

#auth.send_email_verification(user['idToken'])

#auth.send_password_reset_email(email)