import pywhatkit as pywhat
from news_reader.config import config_data
from logger.log import Log
import datetime
from messaging.message import MessageFrame
from messaging.notification import Notification


class WhatsappNotification(Notification):
    def notify(self, articles, title):
        log = Log("Logging")
        try:
            current_hour = datetime.datetime.now().hour
            current_minutes = datetime.datetime.now().minute
            if current_minutes > 57:
                current_hour = current_hour + 1
                current_minutes = 1

            message_frame = MessageFrame("message frame")
            message = message_frame.build_message(articles, title)
            pywhat.sendwhatmsg(
                config_data["whatsapp_sender"], message, current_hour, current_minutes
            )
        except Exception as e:
            log.log_error(e)
