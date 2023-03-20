
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("truedrowning-c7e80-firebase-adminsdk-dgu8c-91e8ee9522.json")
firebase_admin.initialize_app(cred)
