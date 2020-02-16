from django import forms 
from rango.models import Category, Page 

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, 
		help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	#An inline class to provide additional information on the form 
	class Meta: 
		#Provide associate between ModelForm and model 
		model = Category 
		fields = ('name',)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128,
		help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=200, 
		help_text="Please enter the URL of the page.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta: 
		#Provide association between ModelForm and model 
		model = Page
		#we can either exclude the category field from the form 
		#or specify the fields to include 
		# fields = ('title', 'url', 'views')
		exclude	= ('category',)


