# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Article, Sources, Location
# Create your views here.
import requests
import urllib
from xml.etree import ElementTree
import lxml
from random import uniform
import newspaper
import sys
from .models import generateKeys

		
news_sources = [ 
	{'language': 'fr', 'location': 'fr', 'url': 'http://www.20minutes.fr/', 'id': '20minutes', 'description': 'default'},
	{'language': 'il', 'location': 'il', 'url': 'http://www.haaretz.com/', 'id': 'haaretz', 'description': 'default'},
	{'language': 'sy', 'location': 'sy', 'url': 'http://french.irib.ir/info/iran-actualite', 'id': 'irib', 'description': 'default'},
	{'language': 'ir', 'location': 'ir', 'url': 'http://www.iran-daily.com/', 'id': 'irandaily', 'description': 'default'},
	{'language': 'sy', 'location': 'sy', 'url': 'http://www.newsnow.co.uk/h/World+News/Middle+East/Syria', 'id': 'cnewssyria', 'description': 'default'},	
	{'language': 'us', 'location': 'us', 'url': 'https://www.nytimes.com/', 'id': 'nytimes', 'description': 'default'},
	{'language': 'fr', 'location': 'fr', 'url': 'http://www.leparisien.fr/', 'id': 'leparisien', 'description': 'default'},
	{'language': 'fr', 'location': 'fr', 'url': 'http://www.lemonde.fr/international/', 'id': 'lemondeinter', 'description': 'default'},
	{'language': 'fr', 'location': 'fr', 'url': 'http://www.lemonde.fr/societe/', 'id': 'lemondesociete', 'description': 'default'},
	{'language': 'fr', 'location': 'ch', 'url': 'http://www.lematin.ch/', 'id': 'lematin', 'description': 'default'},	
	]

def genNewspaperFromApi():
	for source in news_sources:
		print source['id']
		if Sources.objects.filter(name=source['id']).exists() is False:
			Src = Sources(name=source['id'], key=source['id'], description=source['description'], link=source['url'], country=source['location'], language=source['language'])
			Src.save()
		else:
			Src = Sources.objects.filter(name=source['id']).get()
		n = newspaper.build(source['url'])
		for art in n.articles:

			art.download()
			art.parse()
			art.nlp()
			kw_keys = '%%'.join(map(str,art.keywords))
			if Article.objects.filter(link=art.url).exists() is False:
				a = Article(source=Src, link=art.url, abstract=art.summary, location=retrieveLocation(Src.country), key=kw_keys)
				a.save()
		
def	retrieveLocation(location):
	if Location.objects.filter(country=location).exists() is True:
		return Location.objects.filter(country=location).get()
	args = {"country": location, "username": "gathering"}
	r = requests.get("http://api.geonames.org/search?" + urllib.urlencode(args))
	tree = ElementTree.fromstring(r.text.encode('utf-8'))
	_lat = tree.find('geoname/lat')
	print "lat = " + _lat.text
	_lng = tree.find('geoname/lng')
	print "lng = " + _lng.text

	x = Location.objects.create(country=location, lat=_lat.text, lng=_lng.text)
	x.save()
	#return x.get()
	return x

def	createSource(json):
	for source in json['sources']:
		print source
		x = Sources(name=source['name'], key=source['id'], description=source['description'], link=source['url'], country=source['country'], language=source['language'])
		if Sources.objects.filter(name=source['name']).exists() is False:
			x.save()

def getSource():
	apisources = {"https://newsapi.org/v1/sources?": "06dd8361b57b411d8dba53d500de5a71",}
	for source in apisources.keys():
		args = {"language": "en"}
		r = requests.get(source + urllib.urlencode(args))
		createSource(r.json())


def parseSource(json, Src):
	print json['source']
	for art in json['articles']:
		if Article.objects.filter(link=art['url']).exists() is False:
			try:
				x = Article(source=Src, link=art['url'], abstract=art['description'], location=retrieveLocation(Src.country), key="default")
				x.save()
			except Exception as e:
				print "Unexpected error:", sys.exc_info()[0]

def genArticle():
	for source in Sources.objects.all():
		try:
			print source.id
			#if source.id == "football-italia":
			args = {"apiKey": "06dd8361b57b411d8dba53d500de5a71", "source": source.key, "sortBy": "top"}
			url = "https://newsapi.org/v1/articles?" + urllib.urlencode(args)
			r = requests.get(url)
			if r.status_code is 200:
				print "OK"
				parseSource(r.json(), source)
				print url
		except Exception as e:
			print "Unexpected error:", sys.exc_info()[0]

def retrieve_articles():
	getSource()
	genArticle()
	genNewspaperFromApi()
	#generateKeys()

