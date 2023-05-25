from gnews.news_extractor import NewsExtractor
import requests
from news_reader.config import config_data
from bs4 import BeautifulSoup
from gnews.article import Article
from logger.log import Log
import pytz
import datetime


class NdtvNewsExtractor(NewsExtractor):
    def extract(self, title):
        log = Log("Logging")
        articles = []
        headline = ""
        link = ""
        aimagesrc = ""
        published_date = ""
        f_published_date = ""
        try:
            if title is None:
                title = config_data["default_title"]
            response = requests.get(config_data["ndtv_news_url"] + title)
            soup = BeautifulSoup(response.text, "html.parser")
            news_list = soup.find_all("div", id="news_list")
            list_length = len(news_list)
            for lst_index in range(list_length):
                lst_news = (news_list[lst_index]).find_all("li")
                news_length = len(lst_news)
                for news_index in range(news_length):
                    news = lst_news[news_index]
                    if news.find("a") is not None and "title" in news.find("a").attrs:
                        headline = news.find("a")["title"]
                    if news.find("a") is not None and "href" in news.find("a").attrs:
                        link = news.find("a")["href"]
                    if news.find("img") is not None and "src" in news.find("img").attrs:
                        aimagesrc = news.find("img")["src"]
                    date_text = news.find_all(
                        "span", class_=config_data["ndtv_published_date_class"]
                    )
                    date_array = ((date_text[0]).getText()).split("|")
                    published_date = self.get_utc_date(
                        (date_array[len(date_array) - 1]).strip()
                    )
                    f_published_date = (date_array[len(date_array) - 1]).strip()
                    articles.append(
                        Article(
                            f"{headline}",
                            f"{link}",
                            f"{aimagesrc}",
                            f"{published_date}",
                            f"{f_published_date}",
                        )
                    )
        except Exception as e:
            log.log_error(e)
        return articles

    def get_utc_date(self, in_date):
        formatted_date = None
        log = Log("Logging")
        try:
            date = datetime.datetime.strptime(in_date, "%A %B %d, %Y")
            utc = pytz.timezone("UTC")
            date_utc = utc.localize(date)
            formatted_date = date_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            log.log_error(e)
        return formatted_date
