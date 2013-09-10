from django.contrib.gis import admin

from .models import Hike, Note


admin.site.register(Hike)
admin.site.register(Note, admin.OSMGeoAdmin)