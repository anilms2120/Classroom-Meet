from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import datetime

# Create your views here.


def home(request,prefilled={'title':"",'description':"",'class':'Class'}):

	print(prefilled)
	if request.method=='POST':
		title = request.POST.get('title')
		description = request.POST.get('description')
		group = request.POST.get('class')
		print(group)
		group = Classes.objects.get(name=group)
		print(group)
		teacher = Teacher.objects.get(user=request.user)
		print(title,description,group,teacher)
		article_count = Article.objects.filter(title=title,teacher=teacher).count()
		if not article_count:

			Article.objects.create(title=title,description=description,group=group,teacher=teacher)
			article = Article.objects.get(title=title,description=description,group = group,teacher=teacher)
			for i in group.student_set.all():
				i.articles.add(article)
			return redirect('home')
		else:
			article = Article.objects.filter(title=title,teacher=teacher).first()
			print(article)
			for i in article.group.student_set.all():
				i.articles.remove(article)
			article.description=description
			article.group = group
			article.save()
			for i in article.group.student_set.all():
				i.articles.add(article)
			return redirect('home')
	count = Teacher.objects.filter(user=request.user).count()
	all_classes = Classes.objects.all()
	context = {'count':count,'all_classes':all_classes}
	# prefilled = {'title':"",'description':"",'value':""}
	context['prefilled']=prefilled
	if count == 0:
		student = Student.objects.get(user=request.user)
		classes = student.classes.all()
		articles = student.articles.all().order_by('-date_created')
		assignments = student.assignments.all().order_by('-date_created')
		context['classes']=classes
		context['articles']=articles
		context['assignments']=assignments
		submissions = Submission.objects.filter(name=request.user).all()
		arr = []
		for i in assignments:
			if submissions.filter(assignment=i).first() is not None:
				arr.append(i)
		context['arr']=arr

		return render(request,'main/home.html',context=context)
	else:
		teacher = Teacher.objects.get(user=request.user)
		articles = teacher.article_set.all().order_by('-date_created')
		assignments = teacher.assignment_set.all().order_by('-date_created')
		classes = teacher.classes_set.all()
		context['classes']=classes
		context['articles']=articles
		context['assignments']=assignments
	return render(request,'main/home.html',context = context)

def start(request):

	return redirect(loginpage)


def student_registerpage(request):
	form = CreateUserForm()
	if request.method =='POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				email = form.cleaned_data.get('email')
				Student.objects.create(user=user,name=username,email=email)
				messages.success(request,'User created successfully '+username)
				return redirect('login')
		else:
			messages.error(request,form.errors)
	context = {'form':form}
	return render(request,'main/register.html',context=context)



def teacher_registerpage(request):

	form = CreateUserForm()
	if request.method =='POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				Teacher.objects.create(user=user,name=username)
				messages.success(request,'User created successfully '+username)
				return redirect('login')
		else:
			messages.error(request,form.errors)
	context = {'form':form}
	return render(request,'main/register.html',context=context)


def loginpage(request):

	if request.method=='POST':
		username = request.POST.get("username_form")
		password = request.POST.get('password_form')
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			
			return redirect('home')
		else:
			messages.error(request,"invalid")
	return render(request,'main/login.html')


def logoutpage(request):
	logout(request)
	return redirect('login')

def create_class(request):
	if request.method=='POST':
		name = request.POST.get('name_form')
		description = request.POST.get('description_form')
		teacher = Teacher.objects.get(user=request.user)
		Classes.objects.create(name=name,description=description,teacher=teacher)
		print('success')
		return redirect('home')
	
	return render(request,'main/class.html')


def all_classes(request):

	classes = Classes.objects.all()
	context={'data':classes}
	student_classes = Student.objects.filter(user=request.user).count()
	if not student_classes:
		return redirect('create_class')
	else:
		student_classes = Student.objects.get(user=request.user)
	student_classes = student_classes.classes.all()
	print(student_classes)
	context['student_classes']=student_classes
	return render(request,'main/all_classes.html',context=context)

def add_class(request,pk):

	user = Student.objects.get(user=request.user)
	cl = Classes.objects.get(id=pk)
	user.classes.add(cl)
	return redirect('all_classes')


def remove_class(request,pk):
	user = Student.objects.get(user=request.user)
	cl = Classes.objects.get(id=pk)
	user.classes.remove(cl)
	return redirect('all_classes')

def create_article(request):

	return redirect('home')

def add_assignment(request,prefilled={'title':"",'description':"",'due_date':""}):
	if request.method=='POST':
		title = request.POST.get('title_form')
		description = request.POST.get('description')
		date = request.POST.get('date_form')
		group = request.POST.get('class')
		group = Classes.objects.get(name=group)
		teacher = Teacher.objects.get(user=request.user)
		assignment_count = Assignment.objects.filter(title=title,teacher=teacher).count()
		if not assignment_count:
			Assignment.objects.create(title=title,description=description,due_date=date,group=group,teacher = teacher)
			assignment = Assignment.objects.filter(title=title,description=description,due_date=date,group=group,teacher=teacher).first()
			for i in group.student_set.all():
				i.assignments.add(assignment)
			return redirect('home')
		else:
			assignment = Assignment.objects.filter(title=title,teacher=teacher).first()
			for i in assignment.group.student_set.all():
				i.assignments.remove(assignment)
			assignment.description=description
			assignment.due_date = date
			assignment.group = group
			assignment.save()
			for i in assignment.group.student_set.all():
				i.assignments.add(assignment)
			return redirect('home')
	teacher= Teacher.objects.get(user=request.user)
	all_classes = teacher.classes_set.all()
	context={'all_classes':all_classes}
	context['prefilled']=prefilled
	return render(request,'main/add_assignment.html',context=context)

def student_assignment(request,pk):
	assignment = Assignment.objects.get(id=pk)
	context = {}
	if request.method=='POST':
		request_file = request.FILES['file_form']
		if request_file:
			fs = FileSystemStorage()
			file = fs.save(request_file.name,request_file)
			fileurl = "http://127.0.0.1:8000/media/"+file
			print(fileurl)
			check = Submission.objects.filter(name=request.user,assignment=assignment).count()
			if not check:
				Submission.objects.create(name=request.user,assignment=assignment,files=file,files_url = fileurl) 
			else:
				submission = Submission.objects.get(name=request.user,assignment=assignment)
				submission.files = file
				submission.files_url=fileurl
				submission.save()
			return redirect('home')
			# s = Submission.objects.filter(name=request.user,assignment=assignment).first()
			# print("http://127.0.0.1:8000/media/"+s.files.name)
	count = Teacher.objects.filter(user=request.user).count()
	if count == 0:
		context['assignment']=assignment
		return render(request,'main/assignment.html',context=context)
	else:
		submissions = assignment.submission_set.all()
		context['submissions']=submissions
		context['assignment']=assignment
		for  i in submissions:
			print(i.files_url)
		return render(request,'main/view_assignments.html',context=context)

def view_profile(request):

	user = Student.objects.filter(user=request.user).count()
	if user > 0:
		user = Student.objects.get(user=request.user)
	else:
		user = Teacher.objects.get(user=request.user)
	context = {'user':user}
	return render(request,'main/view_profile.html',context=context)

def edit_profile(request):

	count = Teacher.objects.filter(user=request.user).count()
	if not count:
		user = Student.objects.get(user=request.user)
	else:
		user = Teacher.objects.get(user=request.user)

	context = {'count':count,'user':user}
	if request.method =='POST':
		name = request.POST.get('name_form')
		email = request.POST.get('email_form')
		phone = request.POST.get('phone_form')
		department = request.POST.get('department_form')
		if not count:
			sem = request.POST.get('sem_form')
			student = Student.objects.get(user=request.user)
			student.name = name
			student.email = email
			student.phone = phone
			student.department = department
			student.sem = sem
			student.save()
			return redirect('home')
		else:
			teacher = Teacher.objects.get(user=request.user)
			teacher.name = name
			teacher.email = email
			teacher.phone = phone
			teacher.department = department
			teacher.save()
			return redirect('home')
	return render(request,'main/edit_profile.html',context=context)


def view_teacher(request,pk):

	article = Article.objects.get(id=pk)
	teacher = article.teacher
	print(teacher)
	context={'user':teacher}
	return render(request,'main/view_profile.html',context=context)

def view_student(request,pk):

	student = Submission.objects.get(id=pk).name
	student = Student.objects.get(name=student)
	context={'user':student}
	return render(request,'main/view_profile.html',context=context)

def edit_article(request,pk):

	article = Article.objects.get(id=pk)
	prefilled={}
	prefilled['title']=article
	prefilled['description']=article.description
	prefilled['class']=article.group
	return home(request,prefilled)

def delete_article(request,pk):

	article=Article.objects.get(id=pk)
	if request.method=='POST':
		article.delete()
		return redirect('home')
	return render(request,'main/delete_article.html')

def edit_assignment(request,pk):

	assignment = Assignment.objects.get(id=pk)
	prefilled = {}
	prefilled['title']=assignment.title
	prefilled['description']=assignment.description
	prefilled['due_date']=assignment.due_date
	print(prefilled['due_date'])
	return add_assignment(request,prefilled)

def delete_assignment(request,pk):
	assignment=Assignment.objects.get(id=pk)
	if request.method=='POST':
		assignment.delete()
		return redirect('home')
	return render(request,'main/delete_assignment.html')

def separate_class(request,pk):
	student = Student.objects.get(user=request.user)
	get_class = Classes.objects.get(id=pk)
	article = student.articles.filter(group = get_class).order_by("-date_created")
	assignment = student.assignments.filter(group = get_class).order_by("-date_created")

	context = {'article':article,'assignment':assignment,'class':get_class}
	submissions = Submission.objects.filter(name=request.user).all()
	arr = []
	for i in assignment:
		if submissions.filter(assignment=i).first() is not None:
			arr.append(i)
	context['arr']=arr
	return render(request,'main/separate_class.html',context=context)










