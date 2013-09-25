import re

from django import forms

from rest_framework import serializers
from rest_framework.fields import WritableField

from ..hikes.models import Hike, Note, Position


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


class HikeUUIDField(WritableField):
    type_name = 'HikeUUIDField'
    type_label = 'hike uuid'
    form_field_class = forms.CharField

    def to_native(self, value):
        return value.hike.uuid

    def from_native(self, value):
        try:
            return Hike.objects.get(uuid=value)
        except Hike.DoesNotExist:
            raise forms.ValidationError(
                "Hike with uuid={0} does not exist".format(value))


class PositionSerializer(WritableField):
    type_name = 'Position'
    type_label = 'position'

    def __init__(self, *args, **kwargs):
        super(PositionSerializer, self).__init__(*args, **kwargs)

    def to_native(self, value):
        if value is None:
            return None
        return {"latitude": value.latitude, "longitude": value.longitude}

    def from_native(self, value):
        if value is None or value == '':
            return None
        if isinstance(value, (unicode, str)) and "POINT" in value:
            # Value is coming from browseable API form
            m = re.match('POINT\(([0-9.]+) ([0-9.]+)\)', value)
            if m:
                return Position(latitude=m.group(2), longitude=m.group(1))
            else:
                raise forms.ValidationError("Invalid 'position'")
        elif isinstance(value, dict):
            latitude = value.get("latitude")
            if not latitude:
                raise forms.ValidationError("Missing 'latitude'")
            longitude = value.get("longitude")
            if not longitude:
                raise forms.ValidationError("Missing 'longitude'")
            p = Position(latitude=latitude, longitude=longitude)
            return p
        else:
            raise forms.ValidationError("Invalid 'position'")


class NoteSerializer(DocumentSerializerMixin):
    hike = HikeUUIDField()
    position = PositionSerializer(required=False)

    class Meta:
        model = Note
        fields = ['uuid', 'revision', 'doc_type', 'date', 'text', 'position',
                  'hike']
