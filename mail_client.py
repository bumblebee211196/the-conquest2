import os
import smtplib
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader

MAIL_USER = os.environ.get('MAIL_USER')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class MailClient:

    @classmethod
    def _send_message(cls, message):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MAIL_USER, MAIL_PASSWORD)
            smtp.send_message(message)

    @classmethod
    def send_registration_cofirmation(cls, to_addr, team_name, team_reg_id):
        env = Environment(loader=FileSystemLoader('./templates'))
        template = env.get_template('mail_template.html')
        output = template.render(team_name=team_name, team_reg_id=team_reg_id)
        message = EmailMessage()
        message['From'] = MAIL_USER
        message['To'] = to_addr
        message['Subject'] = 'Team Registration Sucessfull'
        message.add_alternative(output, subtype='html')
        cls._send_message(message)
