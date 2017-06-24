from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from myapp.models import Author, Book, Course, Student, Topic
from myapp.forms import InterestForm, TopicForm, LoginForm, StudentForm, CourseForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Index page
def index(req):
    #topiclist = Topic.objects.all().order_by('subject')[:10]
    if 'username' in req.session:
        firstname = Student.objects.get(username=req.session['username']).first_name
        mycourses = Course.objects.filter(student__username=req.session['username'])
        return render_to_response('myapp/index.html', {'firstname': firstname})
    else:
        courselist = Course.objects.all().order_by('title')[:10]
        return render(req, 'myapp/index.html')

# about page
def about(req):
    if 'username' in req.session:
        firstname = Student.objects.get(username=req.session['username']).first_name
        mycourses = Course.objects.filter(student__username=req.session['username'])
        return render_to_response('myapp/about.html', {'firstname': firstname})
    else:
        courselist = Course.objects.all().order_by('title')[:10]
        return render(req, 'myapp/about.html')

# course page
def courselist(req):
    courselist = Course.objects.all().order_by('title')[:10]
    if 'username' in req.session:
        firstname = Student.objects.get(username=req.session['username']).first_name
        return render_to_response('myapp/course.html', {'courselist': courselist, 'firstname': firstname})
    else:
        return render(req, 'myapp/course.html', {'courselist': courselist})

@login_required
def mycourses(req):
    courselist = Course.objects.all().order_by('title')[:10]
    firstname = Student.objects.get(username=req.session['username']).first_name
    mycourses = Course.objects.filter(student__username=req.session['username'])
    return render(req, 'myapp/course.html', {'mycourses': mycourses, 'courselist': courselist, 'firstname': firstname})

# detail page
def coursedetail(req, course_no):
    #c = Course.objects.get(course_no = course_no)
    c = get_object_or_404(Course, course_no = course_no)
    courseNumber = c.course_no
    cTitle = c.title
    cTextbook = str(c.textbook)
    if 'username' in req.session:
        firstname = Student.objects.get(username=req.session['username']).first_name
        return render_to_response('myapp/coursedetail.html', {'courseNumber': courseNumber, 'cTitle': cTitle, 'cTextbook': cTextbook, 'firstname': firstname})
    else:
        return render(req, 'myapp/coursedetail.html', {'courseNumber': courseNumber, 'cTitle': cTitle, 'cTextbook': cTextbook})

# Import necessary classes and models
# Create your views here.
def topiclist(req):
    topiclist = Topic.objects.all()[:10]
    if 'username' in req.session:
        firstname = Student.objects.get(username=req.session['username']).first_name
        return render_to_response('myapp/topic.html', {'topiclist': topiclist, 'firstname': firstname})
    else:
        return render(req, 'myapp/topic.html', {'topiclist': topiclist})

def topicdetail(req, subject):
    topic = Topic.objects.get(subject = subject)
    if req.method == 'POST':
        form = InterestForm(req.POST)
        if form.is_valid():
            fage = form.cleaned_data['age']
            if form.cleaned_data['interested'] == 1:
                topic.avg_age = (topic.avg_age * topic.num_responses + fage) / (topic.num_responses + 1)
                topic.num_responses += 1
            else:
                topic.avg_age = (topic.avg_age * topic.num_responses + fage) / (topic.num_responses)
            topic.save()
            #return HttpResponseRedirect(reverse('myapp:topicdetail'))
            return render(req, 'myapp/topicdetail.html',{'form':form, 'topic':topic})
        else:
            form = InterestForm()
    elif req.method == 'GET':
        form = InterestForm(req.GET)
    else:
        form = InterestForm()
    return render(req, 'myapp/topicdetail.html',{'form':form, 'topic':topic})

# create a topic
@login_required
def addtopic(req):
    firstname = Student.objects.get(username=req.session['username']).first_name
    topiclist = Topic.objects.all()
    if req.method=='POST':
        form = TopicForm(req.POST)
        if form.is_valid():
            topic = form.save(commit=True)
            topic.num_responses=1
            topic.save()
            return HttpResponseRedirect(reverse('myapp:topic'))
    else:
        form = TopicForm()
    return render(req, 'myapp/addtopic.html', {'form':form, 'topiclist': topiclist, 'firstname': firstname})

# allows a user to register as a Student
def register(req):
    if req.method == 'POST':
        form = StudentForm(req.POST)
        usnm = req.POST['username']
        if usnm.strip():
            if Student.objects.filter(username__exact=usnm):
                return HttpResponse('username has already used, Please change another')
            if form.is_valid():
                usr = form.save(commit=True)
                usr.num_responses=1
                usr.save()
            return HttpResponseRedirect(reverse('myapp:login'))
        else:
            return HttpResponse('Invalid login details.')
    else:
        form = StudentForm()
    return render(req, 'myapp/register.html', {'form':form})

# user login method
def user_login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(req, user)
                req.session['username'] = user.username
                req.session['firstname'] = user.firstname
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(req, 'myapp/login.html')

# logout
@login_required
def user_logout(req):
    try:
        logout(req)
        del req.session['username']
    except:
        pass
    return HttpResponseRedirect(reverse(('myapp:index')))

# contact page
def contact(req):
    if 'username' in req.session:
        firstname = Student.objects.get(username=req.session['username']).first_name
        return render_to_response('myapp/contact.html', {'firstname': firstname})
    else:
        return render(req, 'myapp/contact.html')

@login_required
def changepwd(req):
    firstname = Student.objects.get(username=req.session['username']).first_name
    if req.method=='POST':
        form = StudentForm(req.POST)
        if form.is_valid():
            student = form.save(commit=True)
            student.num_responses=1
            student.save()
            return HttpResponseRedirect(reverse('myapp:logout'))
    else:
        form = StudentForm()
    return render(req, 'myapp/chgpwd.html', {'firstname': firstname})

@login_required
def addcourse(req):
    firstname = Student.objects.get(username=req.session['username']).first_name
    courselist = Course.objects.all()
    if req.method=='POST':
        form = CourseForm(req.POST)
        if form.is_valid():
            course = form.save(commit=True)
            course.num_responses=1
            course.save()
            return HttpResponseRedirect(reverse('myapp:course'))
    else:
        form = CourseForm()
    return render(req, 'myapp/addcourse.html', {'form':form, 'courselist': courselist, 'firstname': firstname})
