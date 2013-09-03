from django.contrib import admin

from .models import Hike, Note


class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'revision', 'doc_type')


class HikeAdmin(DocumentAdmin):
    model = Hike


class NoteAdmin(DocumentAdmin):
    model = Note

admin.site.register(Hike, HikeAdmin)
admin.site.register(Note, NoteAdmin)
