import newspaper

newspaper.languages()
minutes = newspaper.build('http://www.lemonde.fr/')

for article in minutes.articles:
	print article.url
	article.download()
	article.parse()
	print article.summary
