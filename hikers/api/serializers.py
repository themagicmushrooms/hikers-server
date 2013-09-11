from rest_framework import serializers

from ..hikes.models import Hike, Note


class DocumentSerializerMixin(serializers.ModelSerializer):
    doc_type = serializers.SerializerMethodField('get_doc_type')

    def get_doc_type(self, obj):
        return obj.__class__.doc_type_name()


class HikeSerializer(DocumentSerializerMixin):
    owner = serializers.Field(source='owner.email')

    class Meta:
        model = Hike
        fields = ['uuid', 'revision', 'doc_type', 'name', 'date', 'owner']

    def restore_object(self, attrs, instance=None):
        hike = super(HikeSerializer, self).restore_object(attrs, instance)
        hike.owner = self.context['request'].user
        return hike


class NoteSerializer(DocumentSerializerMixin):
    hike_uuid = serializers.SerializerMethodField('get_hike_uuid')
    latitude = serializers.SerializerMethodField('get_latitude')
    longitude = serializers.SerializerMethodField('get_longitude')

    class Meta:
        model = Note
        fields = ['uuid', 'revision', 'doc_type', 'date', 'text', 'latitude',
                  'longitude', 'hike_uuid']

    def get_hike_uuid(self, obj):
        return obj.hike.uuid

    def get_latitude(self, obj):
        return obj.position.y

    def get_longitude(self, obj):
        return obj.position.x
