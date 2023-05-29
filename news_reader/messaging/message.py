from news_reader.config import config_data
from logger.log import Log


class MessageFrame:
    def __init__(self, name):
        self.name = name

    def build_message(self, articles, title):
        log = Log("Logging")
        message = config_data["message_to_text"] + "\n\n"
        try:
            message = message + config_data["message_header"] + title + ":\n\n"
            for index in range(len(articles)):
                if index == 10:
                    break
                article = articles[index]
                message = message + ",\n\n" + article.headline
                message = message + ",\n" + article.link
        except Exception as e:
            log.log_error(e)
        return message
