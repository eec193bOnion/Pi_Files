import os
import firebase_admin
from firebase_admin import credentials, messaging

def send_topic_push(title, body):
    workingDirectory = os.path.dirname(os.path.abspath(__file__))
    cred = credentials.Certificate(workingDirectory+"/truedrowning-c7e80-firebase-adminsdk-dgu8c-91e8ee9522.json")
    tdapp = firebase_admin.initialize_app(cred)
    topic = 'web_app'
    message = messaging.Message(
        notification=messaging.Notification(
        title=title,
        body=body,
        image='https://media.gettyimages.com/id/1041463788/photo/drowning-man.jpg?s=612x612&w=gi&k=20&c=T-m_a1PPjCE5b0yDYXnEznq4qun5SWfIrNAL7gfhB0Q='
    ),
    topic=topic
    )
    messaging.send(message)

#send_topic_push('titleTEST','bodyTEST')
