from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from myapp.models import Author, Book, Course, Student, Topic
from myapp.forms import InterestForm, TopicForm, LoginForm, StudentForm, CourseForm, ChangePwd
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def getTime():  # get current time
    import time
    return time.ctime()

def getCount():  # get current counter
    countfile  = open('count.dat','a+')
    counttext = countfile.read()
    try:
        count = int(counttext)+1
    except:
        count = 1
    countfile.seek(0)
    countfile.truncate()
    countfile.write(str(count))
    countfile.flush()
    countfile.close()
    return count

# Index page
def index(req):
    time = getTime()
    count = getCount()
    if 'username' in req.session:
        firstname = User.objects.get(username=req.session['username']).first_name
        return render_to_response('myapp/index.html', {'firstname': firstname, 'count':count, 'time':time})
    else:
        courselist = Course.objects.all().order_by('title')[:10]
        return render(req, 'myapp/index.html', {'count':count, 'time':time})

# about page
def about(req):
    if 'username' in req.session:
        firstname = User.objects.get(username=req.session['username']).first_name
        return render_to_response('myapp/about.html', {'firstname': firstname})
    else:
        courselist = Course.objects.all().order_by('title')[:10]
        return render(req, 'myapp/about.html')

# course page
def courselist(req):
    courselist = Course.objects.all().order_by('title')[:10]
    if 'username' in req.session:
        firstname = User.objects.get(username=req.session['username']).first_name
        return render(req, 'myapp/course.html', {'courselist': courselist, 'firstname': firstname})
    else:
        return render(req, 'myapp/course.html', {'courselist': courselist})

@login_required
def mycourses(req):
    firstname = User.objects.get(username=req.session['username']).first_name
    if Student.objects.filter(username=req.session['username']):
        mycourses = Course.objects.filter(student__username=req.session['username'])
        return render(req, 'myapp/mycourses.html', {'isstudent': True, 'mycourses': mycourses, 'firstname': firstname})
    else:
        return render(req, 'myapp/mycourses.html', {'isstudent': False, 'firstname': firstname})

# detail page
def coursedetail(req, course_no):
    #c = Course.objects.get(course_no = course_no)
    st = Student.objects.filter(first_name='Wang')
    c = get_object_or_404(Course, course_no = course_no)
    courseNumber = c.course_no
    cTitle = c.title
    cTextbook = str(c.textbook)
    if 'username' in req.session:
        firstname = User.objects.get(username=req.session['username']).first_name
        return render_to_response('myapp/coursedetail.html', {'courseNumber': courseNumber, 'cTitle': cTitle, 'cTextbook': cTextbook, 'firstname': firstname})
    else:
        return render(req, 'myapp/coursedetail.html', {'courseNumber': courseNumber, 'cTitle': cTitle, 'cTextbook': cTextbook})

def topiclist(req):
    topiclist = Topic.objects.all()[:10]

    if 'username' in req.session:
        firstname = User.objects.get(username=req.session['username']).first_name
        return render(req, 'myapp/topic.html', {'topiclist': topiclist, 'firstname': firstname})
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
            if 'username' in req.session:
                firstname = User.objects.get(username=req.session['username']).first_name
                return render(req, 'myapp/topicdetail.html',{'form':form, 'topic':topic, 'firstname': firstname})
            else:
                return render(req, 'myapp/topicdetail.html',{'form':form, 'topic':topic})
        else:
            form = InterestForm()
    elif req.method == 'GET':
        form = InterestForm(req.GET)
    else:
        form = InterestForm()

    if 'username' in req.session:
        firstname = User.objects.get(username=req.session['username']).first_name
        return render(req, 'myapp/topicdetail.html',{'form':form, 'topic':topic, 'firstname': firstname})
    else:
        return render(req, 'myapp/topicdetail.html',{'form':form, 'topic':topic})

# send email for test
def sendemail(request):
    subject,form_email,to = 'subject','tabtu@ttxy.org','tabtu@qq.com'
    text_content = 'This is an important message'
    html_content = u'<b>MAP634 Course Project</b><a href="http://www.ttxy.org">TTXY</a>'
    msg = EmailMultiAlternatives(subject,text_content,form_email,[to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    return HttpResponse(u'Send Email Successfully')

# create a topic
@login_required
def addtopic(req):
    firstname = User.objects.get(username=req.session['username']).first_name
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
        photo = req.FILES['photo']
        if usnm.strip():
            if Student.objects.filter(username__exact=usnm):
                return HttpResponse('username has already used, Please change another')
            if form.is_valid():
                #user = User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password'])
                usr = form.save(commit=True)
                usr.num_responses=1
                usr.save()
                u = User.objects.get(username__exact=usnm)
                u.set_password(form.cleaned_data['password'])
                u.save()
                '''
                phototime = request.user.username + str(time.time()).split('.')[0]
                photo_last = str(photo).split('.')[-1]
                photoname = 'photos/%s.%s'%(phototime, photo_last)
                img = Image.open(photo)
                img.save('media/' + photoname)
                count=UserInfo.objects.filter(user=request.user).update(photo=photoname)
                '''
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
                req.session['firstname'] = user.first_name
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
        firstname = User.objects.get(username=req.session['username']).first_name
        return render_to_response('myapp/contact.html', {'firstname': firstname})
    else:
        return render(req, 'myapp/contact.html')

@login_required
def changepwd(req):
    stu = Student.objects.get(username=req.session['username'])
    firstname = stu.first_name
    if req.method=='POST':
        form = ChangePwd(req.POST)
        if form.is_valid():
            newpasswd = form.cleaned_data['password']
            stu.set_password(newpasswd)
            stu.save()
    else:
        form = ChangePwd()
    return render(req, 'myapp/chgpwd.html', {'form':form, 'firstname': firstname})

@login_required
def addcourse(req):
    firstname = User.objects.get(username=req.session['username']).first_name
    courselist = Course.objects.all()[:10]
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

'''
@login_required
def updateInfo(request):
    if request.method=='POST':
        photo=request.FILES['photo']
        if photo:
            phototime = request.user.username+str(time.time()).split('.')[0]
            photo_last = str(photo).split('.')[-1]
            photoname = 'photos/%s.%s'%(phototime,photo_last)
            img = Image.open(photo)
            img.save('myapp/media/' + photoname)

            count = UserInfo.objects.filter(user=request.user).update(
                photo=photoname
            )
            if count:
                return HttpResponse('Successful')
            else:
                return HttpResponse('Failed')
        return HttpResponse('Image is Empty')
'''
