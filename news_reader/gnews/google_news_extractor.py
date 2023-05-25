from gnews.news_extractor import NewsExtractor
import requests
from news_reader.config import config_data
from bs4 import BeautifulSoup
from gnews.article import Article
from logger.log import Log


class GoogleNewsExtractor(NewsExtractor):
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
            response = requests.get(config_data["google_news_url"] + title)
            soup = BeautifulSoup(response.text, "html.parser")
            article_elements = soup.find_all(config_data["google_article_tag"])
            article_images = soup.find_all(config_data["google_article_image_tag"])
            arlength = len(article_elements)
            for arindex in range(arlength):
                article = article_elements[arindex]
                headline_element = article.find(
                    "h3", class_=config_data["article_class"]
                )
                time_element = article.find(
                    "time", class_=config_data["google_published_date_class"]
                )
                published_date = (
                    time_element[config_data["google_published_date_tag"]]
                ).strip()
                f_published_date = (time_element.getText()).strip()
                if headline_element:
                    headline = headline_element.text
                    link = config_data["article_link"] + article.find("a")["href"]
                    if len(article_images) > arindex:
                        aimage = article_images[arindex]
                        if aimage is not None:
                            aimage_element = aimage.find(
                                "img", class_=config_data["image_class"]
                            )
                            aimagesrc = aimage_element.get("src")
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
