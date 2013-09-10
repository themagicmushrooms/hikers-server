from django.contrib.gis import admin

from .models import Hike, Note


class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'revision', 'doc_type')


class DocumentGeoAdmin(admin.OSMGeoAdmin):
    readonly_fields = ('uuid', 'revision', 'doc_type')


class HikeAdmin(DocumentAdmin):
    model = Hike


class NoteAdmin(DocumentGeoAdmin):
    model = Note

admin.site.register(Hike, HikeAdmin)
admin.site.register(Note, NoteAdmin)
