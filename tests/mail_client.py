import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from PIL import Image
from io import BytesIO
from config.auth import SENDER, PASSWORD

class MailClient():
    @staticmethod
    def send_email(html, recipients, pressure_img_url):
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
        
        msgImage = MailClient.convert_image_to_bytes(pressure_img_url)
        msg.attach(msgImage)
        msg.attach(part1)
        msg.attach(part2)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(SENDER, PASSWORD)
           smtp_server.sendmail(SENDER, recipients, msg.as_string())
        print("Message sent!")

    @staticmethod
    def convert_image_to_bytes(url):
        response = requests.get(URL)
        img = Image.open(BytesIO(response.content))
        img_bytes = BytesIO(response.content)
        img.save(img_bytes, format='PNG') 
        img_bytes.seek(0)  
        msgImage = MIMEImage(img_bytes.read(), _subtype='jpeg')  # Substitua '_subtype' conforme necessário
        msgImage.add_header('Content-ID', '<image1>')
        msgImage.add_header('Content-Disposition', 'inline', filename="teste")
        msgImage.add_header("Content-Transfer-Encoding", "base64")
        return msgImage
