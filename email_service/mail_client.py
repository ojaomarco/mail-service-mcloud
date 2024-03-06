import smtplib
from datetime import datetime
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from config.auth import SENDER, PASSWORD


class MailClient():
    @staticmethod
    def send_email(html, recipients):
        text = "Multipet Sopradoras"
        body = "MCloud"
        subject = f'MCloud Status {datetime.now()}' 

        msg = MIMEMultipart('alternative')
        # msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER
        msg['To'] = ', '.join(recipients)

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(SENDER, PASSWORD)
           smtp_server.sendmail(SENDER, recipients, msg.as_string())
        print("Message sent!")




