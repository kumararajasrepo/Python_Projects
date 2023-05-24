from django.shortcuts import render
from gnews.consumer import Consumer
from logger.log import Log



def load_news(request):
    try:    
        nwarticles = None
        title = request.GET.get('title')        
        consumer_obj = Consumer("gnews")
        nwarticles = consumer_obj.google_news_extract(title)
        context = {'nwarticles':nwarticles}
        return render(request, 'news_loader/news_space.html',context)
    except Exception as e:
            log = Log("Logging")
            log.write(e)