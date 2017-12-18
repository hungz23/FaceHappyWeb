from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'webcam/$', views.demo, name='demo'),
    url(r'align/$', views.align, name='align'),
    url(r'train/$', views.train, name='align'),
    url(r'getvideo/$', views.getimage, name='getimage'),
    # url(r'^save/$', views.save, name='save')
]
