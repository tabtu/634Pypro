from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^course/$', views.courselist, name = 'course'),
    url(r'^course/(?P<course_no>\d+)/$', views.coursedetail, name = 'coursedetail'),
    url(r'^topic/$', views.topiclist, name = 'topic'),
    url(r'^topic/(?P<subject>\w+)/$', views.topicdetail, name = 'topicdetail'),
    url(r'^addtopic/$', views.addtopic, name = 'addtopic'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^logout/$', views.user_logout, name = 'logout'),
]
