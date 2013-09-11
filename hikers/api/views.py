from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
from hikers.api.serializers import HikeSerializer, NoteSerializer

from ..hikes.models import Hike, Note


class DocumentViewSetMixin(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        revision = self.request.QUERY_PARAMS.get('revision')
        if not revision:
            data = {
                "error": "You must specify a 'revision' query parameter"
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)
        if obj.revision != self.request.QUERY_PARAMS['revision']:
            data = {
                "error": ("Conflict, you are trying to delete an old revision "
                          "of this object")
            }
            return Response(data, status=HTTP_409_CONFLICT)
        return super(DocumentViewSetMixin, self).destroy(request, *args,
                                                         **kwargs)


class HikesViewSet(DocumentViewSetMixin):
    model = Hike
    serializer_class = HikeSerializer

    def get_queryset(self):
        queryset = Hike.objects.filter(owner=self.request.user)
        return queryset


class NotesViewSet(DocumentViewSetMixin):
    model = Note
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.filter(
            hike__owner=self.request.user)
        return queryset
