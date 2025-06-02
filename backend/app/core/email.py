import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os

from app.core.config import settings

# Configuration
SMTP_HOST = settings.SMTP_HOST
SMTP_PORT = settings.SMTP_PORT
SENDER_EMAIL = settings.SMTP_USER

# Template setup
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates", "email")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def render_template(template_name: str, **context) -> str:
    template = env.get_template(template_name)
    return template.render(**context)


def send_email(subject: str, to_email: str, html_body: str):
    message = MIMEMultipart("alternative")
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.sendmail(SENDER_EMAIL, to_email, message.as_string())

    except smtplib.SMTPRecipientsRefused:
        print(f"Recipient refused: {to_email}")
    except smtplib.SMTPSenderRefused:
        print(f"Sender refused: {SENDER_EMAIL}")
    except smtplib.SMTPDataError as e:
        print(f"SMTP data error: {e}")
    except smtplib.SMTPConnectError as e:
        print(f"SMTP connection error: {e}")
    except smtplib.SMTPServerDisconnected as e:
        print(f"SMTP server disconnected: {e}")
    except smtplib.SMTPException as e:
        print(f"General SMTP error: {e}")
