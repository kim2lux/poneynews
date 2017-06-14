# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from .forms import SearchForm
import requests
import urllib
import json
import pprint
# Create your views here.
import operator
from xml.etree import ElementTree
import lxml
from random import uniform
from newspapers.models import Article, Keyword
from collections import Counter




def refresh(request):
	l = []
	form = SearchForm(request.POST or None)
	articles = []
	query = ""
	if request.method == "POST" and form.is_valid():
		query = form.cleaned_data['query'] 
	articledata = Article.tojson(query)
	Keyword(value=query).save()
	keywords = Keyword.objects.values_list('value', flat=True)
	keywords = Counter(keywords).most_common(10)
	for k in keywords:
		l.append(k[0])
	keywords = l
	return render(request, 'apicom/display.html', locals())
