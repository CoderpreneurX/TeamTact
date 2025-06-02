import random
import string


from fastapi import BackgroundTasks
from sqlmodel import Session

from app.crud.team import is_code_unique
from app.core.email import render_template, send_email


def generate_unique_team_code(session: Session):
    charset = string.ascii_uppercase + string.digits  # A-Z + 0-9
    max_attempts = 10000  # Prevent infinite loop in edge cases

    for _ in range(max_attempts):
        code = "".join(random.choices(charset, k=6))
        if is_code_unique(session, code):
            return code

    return None


def send_team_invite_email(to_email: str, invite_link: str, team_name: str):
    subject = f"You’re invited to join {team_name}"
    html_body = render_template(
        "invite.html", invite_link=invite_link, team_name=team_name
    )
    send_email(subject, to_email, html_body)


def queue_team_invite_email(
    background_tasks: BackgroundTasks, to_email: str, invite_link: str, team_name: str
):
    background_tasks.add_task(send_team_invite_email, to_email, invite_link, team_name)
