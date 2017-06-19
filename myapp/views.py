from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from myapp.models import Author, Book, Course, Student, Topic
from myapp.forms import InterestForm, TopicForm, LoginForm, StudentForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Index page
def index(request):
    topiclist = Topic.objects.all().order_by('subject')[:10]
    if 'username' in request.session:
        firstname = Student.objects.get(username=request.session['username']).first_name
        mycourses = Course.objects.filter(student__username=request.session['username'])
        return render_to_response('myapp/index.html', {'firstname': firstname, 'courselist': mycourses, 'topiclist': topiclist})
    else:
        courselist = Course.objects.all().order_by('title')[:10]
        return render(request, 'myapp/index.html', {'courselist': courselist, 'topiclist': topiclist})


# about page
@login_required
def about(request):
    return render(request, 'myapp/about.html')

# course page
def courselist(request):
    courselist = Course.objects.all()[:10]
    return render(request, 'myapp/course.html', {'courselist': courselist})

# detail page
def coursedetail(request, course_no):
    #c = Course.objects.get(course_no = course_no)
    c = get_object_or_404(Course, course_no = course_no)
    courseNumber = c.course_no
    cTitle = c.title
    cTextbook = str(c.textbook)
    return render(request, 'myapp/coursedetail.html', {'courseNumber': courseNumber, 'cTitle': cTitle, 'cTextbook': cTextbook})


# Import necessary classes and models
# Create your views here.
def topiclist(request):
    topiclist = Topic.objects.all()[:10]
    return render(request, 'myapp/topic.html', {'topiclist': topiclist})

def topicdetail(request, subject):
    tid = Topic.objects.get(subject = subject)
    if request.method == 'POST':
        form1 = InterestForm(request.POST)
        if form1.is_valid():
            interest = form1.save(commit=False)
            interest.num_responses = 1
            interest.save()
            return HttpResponseRedirect(reverse('myapp:topicdetail'))
        else:
            form1 = InterestForm()
    if request.method == 'GET':
        form1 = InterestForm(request.GET)
    return render(request, 'myapp/topicdetail.html',{'tform':form1,'tid': tid})


def addtopic(request):
    topiclist = Topic.objects.all()
    if request.method=='POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=True)
            topic.num_responses=1
            topic.save()
            return HttpResponseRedirect(reverse('myapp:topic'))
    else:
        form = TopicForm()
    return render(request, 'myapp/addtopic.html', {'form':form, 'topiclist': topiclist})


# allows a user to register as a Student
def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        #uf = StudentForm(request.POST)
        usnm = request.POST['username']
        #err = 'invalid content,please input again!'
        if usnm.strip():
            #username = uf.cleaned_data['username']
            #password = uf.cleaned_data['password']
            #address = uf.cleaned_data['address']
            #city = uf.cleaned_data['city']
            #province = uf.cleaned_data['province']
            #age = uf.cleaned_data['age']
            if Student.objects.filter(username__exact=usnm):
                return HttpResponse('username has already used, Please change another')
            if form.is_valid():
                usr = form.save(commit=True)
                usr.num_responses=1
                usr.save()
            request.session['username'] = usnm
            return HttpResponseRedirect(reverse('myapp:index'))
        else:
            return HttpResponse('Invalid login details.')
    else:
        form = StudentForm()
    return render(request, 'myapp/register.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['username'] = user.username
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


# logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def regsuc(req):
    username = req.session.get('username')
    return render_to_response('myapp/regsuc.html', {'username': username})
