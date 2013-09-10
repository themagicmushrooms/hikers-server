from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'hikes', views.HikesViewSet)
router.register(r'notes', views.NotesViewSet)

# We include the login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^document/(?P<uuid>[\w:@\.-]+)/', views.get_document,
        name='get_document'),
    url(r'^document/(?P<uuid>[\w:@\.-]+)?(?P<rev>[\w:@\.-]+)',
        views.delete_document, name='delete_document'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
