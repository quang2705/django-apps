from django.shortcuts import render
from django.http import HttpResponse 
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm

def index(request): 
	#Query the database for list of ALL categories currently stored
	#Order the category by the number of likes
	#Retrieve the top 5 only
	#place the list in our context_dict 
	#pass context_dict to the template engine

	#construct a dictionary to pass to the template engine as its context
	#Note the key boldmessage is the same as {{boldmessage}} in the template

	# context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by("-views")[:5]
	context_dict = {'categories': category_list, 'pages': page_list}


	#render the response and send it back
	return render(request, 'rango/index.html', context=context_dict)

def about(request): 
	return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
	#Create a context dictionary which we can pass 
	#to the template readering engine
	context_dict = {}

	try:
		#can we find the category name slug with the
		#given parameter
		#If we cant the get() raise a DoesNotExist exception
		category = Category.objects.get(slug=category_name_slug)
		
		#Retrieve all the associated page
		#filter() will return a list of page objects or empty list
		pages = Page.objects.filter(category=category)

		#add result list to the context dict 
		context_dict['pages'] = pages
		#we all so add the category object to verify in the 
		#template 
		context_dict['category'] = category
	except Category.DoesNotExist:
		#get here if we didn't find the category
		#dont do anything
		context_dict['pages'] = None
		context_dict['category'] = None
	#render the response and return to the client 
	return render(request, 'rango/category.html', context_dict)

def add_category(request): 
	form = CategoryForm()

	#A HTTP POST?
	if (request.method == 'POST'): 
		form = CategoryForm(request.POST)
		print(request.POST)

		#Is it a valid form 
		if form.is_valid(): 
			#Save the new category to the database
			form.save(commit=True)
			#We can give a confirmation message or direct the user 
			#back to the index page
			return index(request)
		else:
			print(form.errors)

	#will handle the bad form , new form, or no form supplied cases
	#Render the form with error message (if any)
	return render(request, 'rango/add_category.html', {'form':form})