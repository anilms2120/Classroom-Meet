from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
	user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	name = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True)
	department = models.CharField(max_length=500,null=True)
	phone = models.CharField(max_length=200,null=True)
	password = models.CharField(max_length=100,null=True,blank=False)

	def __str__(self):
		return self.name

class Classes(models.Model):
	name = models.CharField(max_length=200,null=True)
	teacher = models.ForeignKey(Teacher,null=True,on_delete=models.SET_NULL)
	description = models.TextField(max_length=1000,null=True)


	def __str__(self):
		return self.name



class Article(models.Model):
	title = models.CharField(max_length=200,null=True)
	teacher = models.ForeignKey(Teacher,null=True,on_delete=models.SET_NULL)
	description = models.TextField(max_length=1000,null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True)
	group = models.ForeignKey(Classes,null=True,on_delete=models.SET_NULL)

	def __str__(self):
		return self.title




class Assignment(models.Model):
	title = models.CharField(max_length=200,null=True)
	teacher = models.ForeignKey(Teacher,null=True,on_delete=models.SET_NULL)
	description = models.TextField(max_length=1000,null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True)
	group = models.ForeignKey(Classes,null=True,on_delete=models.SET_NULL)
	due_date = models.DateTimeField(null=True)

	def __str__(self):
		return self.title

class Submission(models.Model):
	name = models.CharField(max_length=200,null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True)
	assignment = models.ForeignKey(Assignment,null=True,on_delete=models.SET_NULL)
	files = models.FileField(null=True)
	files_url = models.CharField(max_length=500,null=True)

	def __str__(self):
		return self.name


class Student(models.Model):
	user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE) 
	name = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True)
	department = models.CharField(max_length=500,null=True)
	phone = models.CharField(max_length=200,null=True)
	sem = models.CharField(max_length=200,null=True)
	password = models.CharField(max_length=100,null=True,blank=False)
	classes = models.ManyToManyField(Classes)
	articles = models.ManyToManyField(Article)
	assignments = models.ManyToManyField(Assignment)

	def __str__(self):
		return self.name
 

