from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions
from rest_framework.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
from hikers.api.serializers import (TYPE_TO_SERIALIZER_CLASS_MAP,
                                    HikeSerializer, NoteSerializer)

from ..hikes.models import Document, Hike, Note
from ..hikes.models import TYPE_TO_CLASS_MAP


class DocumentView(generics.RetrieveDestroyAPIView):
    lookup_field = 'uuid'
    model = Document

    def get_object(self, queryset=None):
        document = super(DocumentView, self).get_object(queryset)
        self.doc_type = document.doc_type
        doc_class = TYPE_TO_CLASS_MAP[self.doc_type]
        full_document = doc_class.objects.get(uuid=document.uuid)
        return full_document

    def get_serializer_class(self):
        return TYPE_TO_SERIALIZER_CLASS_MAP[self.doc_type]


class GetDocumentView(DocumentView):
    pass
get_document = GetDocumentView.as_view()


class DeleteDocumentView(DocumentView):
    pass
delete_document = DeleteDocumentView.as_view()


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
