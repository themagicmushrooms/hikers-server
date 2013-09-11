from django.contrib.gis import forms as gis_forms
from django import forms

from rest_framework import serializers
from rest_framework.fields import WritableField

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


class PointField(WritableField):
    type_name = 'PointField'
    type_label = 'point'
    form_field_class = gis_forms.GeometryField

    def to_native(self, value):
        return {"latitude": value.y, "longitude": value.x}

    def from_native(self, value):
        geometry_field = self.form_field_class()
        if isinstance(value, (unicode, str)) and "Point" in value:
            # Value is coming from browseable API form
            return geometry_field.clean(value)
        elif isinstance(value, dict):
            latitude = value.get("latitude")
            if not latitude:
                raise forms.ValidationError("Missing 'latitude'")
            longitude = value.get("longitude")
            if not longitude:
                raise forms.ValidationError("Missing 'longitude'")
            new_value = "Point ({0} {1})".format(longitude, latitude)
            return geometry_field.clean(new_value)
        else:
            raise forms.ValidationError("Invalid 'position'")


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


class NoteSerializer(DocumentSerializerMixin):
    hike = HikeUUIDField()
    position = PointField()

    class Meta:
        model = Note
        fields = ['uuid', 'revision', 'doc_type', 'date', 'text', 'position',
                  'hike']
