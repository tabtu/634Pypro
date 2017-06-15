from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Author, Book, Course, Student
from django.shortcuts import get_object_or_404


# Create your views here.


# index page
def index(request):
    courselist = Course.objects.all().order_by('title')[:10]
    return render(request, 'myapp/index0.html', {'courselist': courselist})


# about page
def about(request):
    return render(request, 'myapp/about0.html')

# course page
def course(request):
    courselist = Course.objects.all() [:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of courses: ' + '</p>'
    response.write(heading1)
    for course in courselist:
        para = '<p>' + str(course) + '</p>'
        response.write(para)
    return response


# detail page
def detail(request, course_no):
    #c = Course.objects.get(course_no = course_no)
    c = get_object_or_404(Course, course_no = course_no)
    courseNumber = c.course_no
    cTitle = c.title
    cTextbook = str(c.textbook)
    return render(request, 'myapp/detail0.html', {'courseNumber': courseNumber, 'cTitle': cTitle, 'cTextbook': cTextbook})


# Import necessary classes and models
# Create your views here.
def topics(request):
    topiclist = Topic.objects.all()[:10]
    return render(request, 'myapp/topic.html', {'topiclist': topiclist})


# Import necessary classes and models
# Create your views here.
def addtopic(request):
    topiclist = Topic.objects.all()
    if request.method=='POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.num_responses=1
            topic.save()
            return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form=TopicForm()
    return render(request, 'myapp/addtopic.html', {'form': form, 'topiclist': topiclist})
