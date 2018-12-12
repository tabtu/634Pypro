from django.conf.urls import url
from . import views
from django.conf.urls import include

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^detail/', views.detail('Network'), name='detail'),
]

url(r'^lab3_db/', include('lab3_db.urls',namespace='lab3_db'))