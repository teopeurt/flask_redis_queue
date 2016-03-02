__author__ = 'teopeurt'
from flask.ext.mail import Message, Mail
from flask import Flask, current_app


def send_email(msg):
    from routes import app
    with app.app_context():
        mail = Mail()
        mail.init_app(current_app)
        print("hallo world")
        mail.send(msg)
