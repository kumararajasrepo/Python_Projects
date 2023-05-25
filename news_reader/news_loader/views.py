from django.shortcuts import render
from gnews.news_articles import NewsArticles
from logger.log import Log


def load_news(request):
    log = Log("Logging")
    context = None
    try:
        nwarticles = None
        title = request.GET.get("title")
        news_obj = NewsArticles("gnews")
        nwarticles = news_obj.get_news_aricles(title)
        context = {"nwarticles": nwarticles}
    except Exception as e:
        log.log_error(e)
    return render(request, "news_loader/news_space.html", context)
