from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect 
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

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

def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()
	if (request.method == 'POST'): 
		form = PageForm(request.POST)
		#Is it a valid form 
		if form.is_valid(): 
			if category:
				print(category)
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)
	context_dict = {'form': form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)

def register(request): 
	#A boolean value telling the template whether 
	#the registration was successfule
	#set false init. code change to true when register 
	#success 
	registered = False
	user_form = UserForm()
	profile_form = UserProfileForm()
	#if it is a HTTP Post, we process the data
	if request.method == 'POST': 
		#grap information from the raw form info
		#make use of both UserForm and UserProfileForm 

		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#If the two forms are valid: 
		if user_form.is_valid() and profile_form.is_valid(): 
			#save the user form data to the db
			user = user_form.save()

			#hash the password with the set_password method 
			#after hashed update the user object
			user.set_password(user.password)
			user.save()

			#sort the UserProfile instance 
			#need to set the user attribute ourselves 
			# set commit = False. This delays saving the model until 
			#we ready to avoid integrity problems 

			profile = profile_form.save(commit=False)
			profile.user = user

			#Did the user provide a profile picture? 
			# If so, get it in the input form and put it in the 
			# UserProfile model 
			if 'picture' in request.FILES: 
				profile.picture = request.FILES['picture']

			#Save the UserProfile mode instance 
			profile.save()

			#Update our variable to indicate the the template registration
			#was successful 
			registered = True 
		else:
			print(user_form.errors, profile_form.errors)

	context_dict ={'user_form': user_form, 'profile_form':profile_form, 'registered': registered}
	return render(request, 'rango/register.html', context_dict) 

def user_login(request): 
	#If the request if a HTTP POST, try to pull out the relevant information 
	if request.method == "POST": 
		#Gather the username and password provided by the users. 
		#This information is obtained from the login form 
		#user request.POST.get('<variable>') instead of request.POST['<variable>']
		#because the later one result in KeyError

		username = request.POST.get('username')
		password = request.POST.get('password')

		#use Django machinary to see if username/password combination
		#is valid - a user object is return of it is 
		user = authenticate(username=username, password=password)

		#if we have a user object, authenticate, 
		#otherwise python returns None 
		if user: 
			# is the account activate
			if user.is_active: 
				#if the account is valid and active, we log user in
				#send the user to the home page
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse('Your Rango account is disabled')
		else:
			#Bad login details were provided. Can't log the user in 
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied")
	#The request is not a HTTP POST
	else:
		#no context variable to pass to system 
		#return blank login page
		return render(request, 'rango/login.html', {})
