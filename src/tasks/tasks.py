import smtplib
from email.message import EmailMessage
from celery import Celery
from config import GMAIL_PASSWORD, SMTP_USER

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465


celery = Celery('tasks', broker='redis://localhost:6379')


def get_email(username: str):
    email = EmailMessage()
    email['Subject'] = 'Письмо'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER
    email.set_content(f'Привет {username}, это моё первое письмо')
    return email


@celery.task
def send_email_report(username: str):
    email = get_email(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, GMAIL_PASSWORD)
        server.send_message(email)
