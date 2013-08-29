from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.my_hikes, name='my_hikes'),
    url(r'^detail/(?P<uuid>[\w:@\.-]+)/$', views.hike_detail,
        name='hike_detail'),
)
