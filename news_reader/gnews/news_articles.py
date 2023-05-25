from gnews.article import Article
from logger.log import Log
import pandas as pd
from gnews.google_news_extractor import GoogleNewsExtractor
from gnews.ndtv_news_extractor import NdtvNewsExtractor


class NewsArticles:
    def __init__(self, name):
        self.name = name

    def create_news_extractor(self, source):
        if source == "google":
            return GoogleNewsExtractor()
        elif source == "ndtv":
            return NdtvNewsExtractor()
        else:
            raise ValueError("Invalid news source")

    def get_news_aricles(self, title):
        sorted_articles = []
        log = Log("Logging")
        try:
            news_extractor = self.create_news_extractor("google")
            news = news_extractor.extract(title)
            news_extractor = self.create_news_extractor("ndtv")
            news.extend(news_extractor.extract(title))
            df = pd.DataFrame([vars(article) for article in news])
            df_sorted = df.sort_values("published_date", ascending=False)
            for _, row in df_sorted.iterrows():
                article = Article(
                    headline=row["headline"],
                    link=row["link"],
                    aimage=row["aimage"],
                    published_date=row["published_date"],
                    f_published_date=row["f_published_date"],
                )
                sorted_articles.append(article)
        except Exception as e:
            log.log_error(e)
        return sorted_articles
