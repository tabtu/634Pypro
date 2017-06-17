from django.conf.urls import url
from . import views, search

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^course/$', views.course, name = 'course'),
    url(r'^(?P<course_no>\d+)/$', views.detail, name = 'detail'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^search-form$', search.search_form),
    url(r'^search$', search.search),
    url(r'^topics/(?P<topic_id>/\d+)/$', views.topics, name = 'topic'),
]
