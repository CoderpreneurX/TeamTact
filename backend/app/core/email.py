import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import os

from app.core.config import settings

# Configuration
SMTP_HOST = settings.SMTP_HOST
SMTP_PORT = settings.SMTP_PORT  # Mailpit default
SENDER_EMAIL = settings.SMTP_USER

# Template setup
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates", "email")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def render_template(template_name: str, **context) -> str:
    template = env.get_template(template_name)
    return template.render(**context)


def send_invite_email(to_email: str, invite_link: str, team_name: str):
    subject = f"You’re invited to join {team_name}"
    html_body = render_template("invite.html", invite_link=invite_link, team_name=team_name)

    message = MIMEMultipart("alternative")
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.sendmail(SENDER_EMAIL, to_email, message.as_string())
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
