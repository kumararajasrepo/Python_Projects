from news_reader.config import config_data
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger.log import Log
from messaging.message import MessageFrame
from messaging.notification import Notification


class EmailNotification(Notification):
    def notify(self, articles, title):
        log = Log("Logging")
        try:
            sender_email = config_data["sender_email"]
            receiver_email = config_data["receiver_email"]
            subject = config_data["subject"]
            message_frame = MessageFrame("message frame")
            message = message_frame.build_message(articles, title)
            email_message = MIMEMultipart()
            email_message["From"] = sender_email
            email_message["To"] = receiver_email
            email_message["Subject"] = subject
            email_message.attach(MIMEText(message, "plain"))
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = config_data["smtp_username"]
            smtp_password = config_data["smtp_password"]
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, email_message.as_string())
        except Exception as e:
            log.log_error(e)
