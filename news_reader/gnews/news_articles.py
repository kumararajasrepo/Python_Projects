from gnews.article import Article
from logger.log import Log
import pandas as pd
from gnews.google_news_extractor import GoogleNewsExtractor
from gnews.ndtv_news_extractor import NdtvNewsExtractor
from gnews.news_sources import NewsSources
from messaging.email import EmailNotification
from messaging.whatsapp import WhatsappNotification
from messaging.notification_sources import NotificationSources


class NewsArticles:
    def __init__(self, name):
        self.name = name

    def create_news_extractor(self, source):
        if source == NewsSources.GOOGLE.value:
            return GoogleNewsExtractor()
        elif source == NewsSources.NDTV.value:
            return NdtvNewsExtractor()
        else:
            raise ValueError("Invalid news source")

    def get_news_aricles(self, title):
        sorted_articles = []
        news = []
        log = Log("Logging")
        try:
            for source in NewsSources:
                news_extractor = self.create_news_extractor(source.value)
                news.extend(news_extractor.extract(title))
            df_sorted = self.sort_news_aricles(news)
            sorted_articles = self.build_articles(df_sorted)
            self.notify(sorted_articles, title)
        except Exception as e:
            log.log_error(e)
        return sorted_articles

    def sort_news_aricles(self, news):
        df_sorted = None
        log = Log("Logging")
        try:
            df = pd.DataFrame([vars(article) for article in news])
            df_sorted = df.sort_values("published_date", ascending=False)
        except Exception as e:
            log.log_error(e)
        return df_sorted

    def build_articles(self, data_frame):
        articles = []
        log = Log("Logging")
        try:
            for _, row in data_frame.iterrows():
                article = Article(
                    headline=row["headline"],
                    link=row["link"],
                    aimage=row["aimage"],
                    published_date=row["published_date"],
                    f_published_date=row["f_published_date"],
                )
                articles.append(article)
        except Exception as e:
            log.log_error(e)
        return articles

    def get_notification_source(self, source):
        log = Log("Logging")
        notify_obj = None
        try:
            if source == NotificationSources.EMAIL.value:
                notify_obj = EmailNotification()
            elif source == NotificationSources.WHATSAPP.value:
                notify_obj = WhatsappNotification()
            else:
                raise ValueError("Invalid notification source")
        except Exception as e:
            log.log_error(e)
        return notify_obj

    def notify(self, articles, title):
        log = Log("Logging")
        try:
            for source in NotificationSources:
                notify_obj = self.get_notification_source(source.value)
                if notify_obj is not None:
                    notify_obj.notify(articles, title)
        except Exception as e:
            log.log_error(e)
