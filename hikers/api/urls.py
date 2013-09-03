from django.conf.urls import patterns, url, include

from . import views


# We include the login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^document/(?P<uuid>[\w:@\.-]+)/', views.get_document,
        name='get_document'),
    url(r'^document/(?P<uuid>[\w:@\.-]+)?(?P<rev>[\w:@\.-]+)',
        views.delete_document, name='delete_document'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
