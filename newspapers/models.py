# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json
import random
# Create your models here.
from collections import Counter

keywordsToDel = ['taken', 'default', 'way', 'une', 'achat', 'dans']

def generateKeys():
	Keyword.reset()
	rawkey = Article.objects.values_list('key', flat=True)
	keys = [a for a in rawkey]
	for idx, k in enumerate(keys):
		keys.extend(k.split('%%'))
		keys.remove(k)
	for k in keys:
		print k
	print "*******************************"
	#v = list(set(keys) - set(keywordsToDel))
	v = [x for x in keys if x not in keywordsToDel]
	count = Counter(v)
	res = count.most_common(50)
	print res
	for k in res:
		Keyword(value=k[0]).save()

class Keyword(models.Model):
	value = models.CharField(max_length=30)
	
	def __str__(self):
		return self.value
	@classmethod
	def reset(cls):
		Keyword.objects.all().delete()


class Location(models.Model):
	country = models.CharField(max_length=30)
	lat = models.FloatField()
	lng = models.FloatField()
	def __str__(self):
		return self.country + str(self.lat) + str(self.lng)
	def __tojson__(self):
		elem = {}
		elem['lat'] = str(float(self.lat) + random.uniform(-0.5, 0.5))
		elem['lng'] = str(float(self.lng) + random.uniform(-0.5, 0.5))
		return elem

class Sources(models.Model):
	name = models.CharField(max_length=30)
	key = models.CharField(max_length=30)
	link = models.CharField(max_length=30)
	language = models.CharField(max_length=30)
	country = models.CharField(max_length=30)
	description = models.CharField(max_length=30)
	
	def __str__(self):
		return self.name + self.link
	def __tojson__(self):
		elem = {}
		elem['name'] = self.name
		elem['country'] = self.country
		return elem
		
class Article(models.Model):
	source = models.ForeignKey(Sources)
	link = models.CharField(max_length=30)
	location = models.ForeignKey(Location)
	key = models.CharField(max_length=30)
	date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="added time")
	abstract = models.CharField(max_length=200)

	
	def __str__(self):
		return self.abstract + self.key
	@classmethod
	def tojson(cls, query):
		marker = []
		for article in Article.objects.filter(abstract__contains=query):
			elem = {}
			elem['source'] = {}
			elem['source'] = article.source.__tojson__()
			elem['link'] = article.link
			elem['key'] = article.key
			elem['abstract'] = elem['source']['name'] + ": " + article.abstract
			elem['location'] = {}
			elem['location'] = article.location.__tojson__()
			marker.append(elem)
		return json.dumps(marker)
		
		
class Useless(models.Model):
	source = models.ForeignKey(Sources)
	link = models.CharField(max_length=30)
	location = models.ForeignKey(Location)
	key = models.CharField(max_length=30)
	date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="added time")
	abstract = models.CharField(max_length=200)
	def __init__():
		pass
	
	def __str__(self):
		return self.date + " => " + self.abstract + self.key