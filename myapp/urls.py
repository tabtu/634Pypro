from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^course/$', views.course, name = 'course'),
    url(r'^(?P<course_no>\d+)/$', views.detail, name = 'detail'),
    url(r'^topics/(?P<topic_id>/\d+)/$', views.topics, name = 'topic'),
]
