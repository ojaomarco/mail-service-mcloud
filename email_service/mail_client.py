import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from PIL import Image
from io import BytesIO
from config.auth import SENDER, PASSWORD
from api_consumer.api_client import Client


class MailClient:

    def tempo_atual():
        agora = datetime.now()
        data_e_hora_formatadas = agora.strftime("%Y-%m-%d %H:%M:%S")
        return data_e_hora_formatadas

    @staticmethod
    def send_email(
        html,
        recipients,
    ):
        text = "Multipet Sopradoras"
        body = "MCloud"
        subject = f"MCloud Status {datetime.now()}"

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SENDER
        msg["To"] = ", ".join(recipients)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        
        msg.attach(part1)
        msg.attach(part2)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(SENDER, PASSWORD)
            smtp_server.sendmail(SENDER, recipients, msg.as_string())
        print("Mensagem enviada às", MailClient.tempo_atual())
