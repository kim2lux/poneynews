from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'', views.retrieve_articles, name='retrieve_articles'),
]