import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
	'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
	#a dictionary of pages you want to populate in 
	#the database

	python_pages = [
		{"title": "Official Python Tutorial", 
		"url":"http://docs.python.org/2/tutorial/", 
		"views": 1}, 
		{"title": "How to Think like a Computer Scientist", 
		"url": "http://www.greenteapress.com/thinkpython/", 
		"views": 3},
		{"title": "Learn Python in 10 Minutes", 
		"url": "http://www.korokithakis.net/tutorials/python/",
		"views": 5}]

	django_pages = [
		{"title":"Official Django Tutorial",
		"url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/", 
		"views": 2},
		{"title":"Django Rocks",
		"url":"http://www.djangorocks.com/",
		"views": 4},
		{"title":"How to Tango with Django",
		"url":"http://www.tangowithdjango.com/", 
		"views": 6}]

	other_pages = [
		{"title":"Bottle",
		"url":"http://bottlepy.org/docs/dev/", 
		"views": 7},
		{"title":"Flask",
		"url":"http://flask.pocoo.org", 
		"views": 9}]

	comsci_pages = [
		{"title":"What is Computer Science", 
		"url":"https://undergrad.cs.umd.edu/what-computer-science",
		"views": 9},
		{"title":"What can you do with a computer science degree", 
		"url":"https://www.topuniversities.com/student-info/careers-advice/what-can-you-do-computer-science-degree", 
		"views": 8},
		{"title":"Top university for computer science degree", 
		"url": "https://www.timeshighereducation.com/student/what-to-study/computer-science", 
		"views": 7}]

	dota_pages = [
		{"title":"DOTA official page", 
		"url":"http://blog.dota2.com/?l=english", 
		"views": 10},
		{"title":"DOTA2 Wiki", 
		"url":"https://en.wikipedia.org/wiki/Dota_2", 
		"views": 4},
		{"title":"Team OG DOTA2", 
		"url": "https://liquipedia.net/dota2/OG", 
		"views": 5}]

	cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
			"Django": {"pages": django_pages, "views": 64, "likes": 32},
			"Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16},
			"Computer Science": {"pages": comsci_pages, "views": 16, "likes": 8},
			"DOTA2": {"pages": dota_pages, "views": 8, "likes": 4}
			}

	for cat, cat_data in cats.items(): 
		c = add_cat(cat, cat_data["views"], cat_data["likes"])
		for p in cat_data["pages"]: 
			add_page(c, p["title"], p["url"], p["views"])

	for c in Category.objects.all(): 
		for p in Page.objects.filter(category=c): 
			print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0): 
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	p.url = url
	p.views = views
	p.save()
	return p

def add_cat(name, views, likes):
	c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
	c.save()
	return c

if __name__=='__main__': 
	print("Staring Rango population script...")
	populate()