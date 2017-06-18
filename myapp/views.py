from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from myapp.models import Author, Book, Course, Student, Topic
from myapp.forms import InterestForm, TopicForm, LoginForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Index page
def index(request):
    courselist = Course.objects.all().order_by('title')[:10]
    topiclist = Topic.objects.all().order_by('subject')[:5]
    return render(request, 'myapp/index.html', {'courselist': courselist, 'topiclist': topiclist})


# about page
def about(request):
    return render(request, 'myapp/about0.html')

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
    form1 = InterestForm()
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
    return render(request, 'myapp/topicdetail0.html',{'tform':form1,'tid': tid})


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
        form=TopicForm()
    return render(request, 'myapp/addtopic.html', {'form': form, 'topiclist': topiclist})


# allows a user to register as a Student
def register(request):
    if request.method == 'POST':
        uf = StudentForm(request.POST)
        err = 'invalid content,please input again!'
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            address = uf.cleaned_data['address']
            city = uf.cleaned_data['city']
            province = uf.cleaned_data['province']
            age = uf.cleaned_data['age']
            if Student.objects.filter(username__exact=username):
                return render_to_response('myapp/register.html',{'uf':uf,'err':err})
            nstu = Student()
            nstu.username = username
            nstu.password = password
            nstu.address = address
            nstu.city = city
            nstu.province = province
            nstu.age = age
            nstu.save()
            req.session['username'] = username
            return HttpResponseRedirect('/myapp/index')
        else:
            return render_to_response('myapp/register.html',{'uf':uf,'err':err})
    else:
        uf = StudentForm()
    return render_to_response('myapp/register.html',{'uf':uf})

def user_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('myapp/login.html', {'form': form,})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST('username')
            password = request.POST('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render_to_response('myapp/index.html')
            else:
                return render_to_response('myapp/login.html', {'form': form,'password_is_wrong':True}, context_instance=RequestContext(request))
        else:
            return render_to_response('myapp/login.html', {'form': form,}, context_instance=RequestContext(request))


def regsuc(req):
    username = req.session.get('username')
    return render_to_response('myapp/regsuc.html', {'username': username})

# logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

def findstudent(request, usnm):
    usr = Student.objects.get(username = usnm)
    return HttpResponse(usr.address)

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('myapp/login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render_to_response('myapp/index.html', RequestContext(request))
            else:
                return render_to_response('myapp/login.html', RequestContext(request, {'form': form,'password_is_wrong':True}))
        else:
            return render_to_response('myapp/login.html', RequestContext(request, {'form': form,}))
