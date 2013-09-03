from rest_framework import serializers

from ..hikes.models import Hike, Note


class DocumentSerializerMixin(serializers.ModelSerializer):
    doc_type = serializers.SerializerMethodField('get_doc_type')

    def get_doc_type(self, obj):
        return obj.__class__.doc_type_name()


class HikeSerializer(DocumentSerializerMixin):
    owner = serializers.SerializerMethodField('get_owner')

    class Meta:
        model = Hike
        fields = ['uuid', 'revision', 'doc_type', 'owner', 'name', 'date']

    def get_owner(self, obj):
        return obj.owner.email


class NoteSerializer(DocumentSerializerMixin):
    hike_uuid = serializers.SerializerMethodField('get_hike_uuid')

    class Meta:
        model = Note
        fields = ['uuid', 'revision', 'doc_type', 'date', 'text', 'hike_uuid']

    def get_hike_uuid(self, obj):
        return obj.hike.uuid


# TODO build this by introspection?
TYPE_TO_SERIALIZER_CLASS_MAP = {
    Hike.doc_type_name(): HikeSerializer,
    Note.doc_type_name(): NoteSerializer
}
