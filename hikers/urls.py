from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^hiking_albums_in_a_trice/$', views.landing, name='landing'),
)
