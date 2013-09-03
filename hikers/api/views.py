from rest_framework import generics
from hikers.api.serializers import TYPE_TO_SERIALIZER_CLASS_MAP

from ..hikes.models import Document
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
