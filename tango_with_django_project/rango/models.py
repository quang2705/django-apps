from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
str_max_length = 128
class Category(models.Model): 
	name = models.CharField(max_length=str_max_length, unique = True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs): 
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	class Meta: 
		verbose_name_plural = 'Categories'

	def __str__(self): 
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=str_max_length)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __str__(self):
		return self.title

class UserProfile(models.Model): 
	#This line is required. Links UserProfile to a User model instance 
	user = models.OneToOneField(User)

	#The additional attributes we wish to include 
	website = models.URLField(blank=True)
	#upload profile will be stored in media folder
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self): 
		return self.user.username
