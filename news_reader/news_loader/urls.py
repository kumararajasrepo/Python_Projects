from django.urls import path
from . import views

urlpatterns = [
    path('',views.load_news,name = 'news'),
    path('news',views.load_news,name = 'news'),
]
    