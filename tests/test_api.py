from django.core.urlresolvers import reverse

from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.test import APITestCase

from tests.factories import HikeFactory, NoteFactory


class HikesTest(APITestCase):
    def test_get_not_found(self):
        url = reverse('get_document', args=['dummy'])
        self.client.get(url, status=HTTP_404_NOT_FOUND)

    def test_get_hike(self):
        hike = HikeFactory.create()
        url = reverse('get_document', args=[hike.uuid])
        response = self.client.get(url, status=HTTP_200_OK)
        self.assertDictContainsSubset({'uuid': hike.uuid}, response.data)
        self.assertDictContainsSubset({'revision': hike.revision},
                                      response.data)
        self.assertDictContainsSubset({'doc_type': 'hike'}, response.data)
        self.assertDictContainsSubset({'owner': hike.owner.email},
                                      response.data)
        self.assertDictContainsSubset({'name': hike.name}, response.data)
        self.assertDictContainsSubset({'date': hike.date}, response.data)

    def test_get_note(self):
        note = NoteFactory.create()
        url = reverse('get_document', args=[note.uuid])
        response = self.client.get(url, status=HTTP_200_OK)
        self.assertDictContainsSubset({'uuid': note.uuid}, response.data)
        self.assertDictContainsSubset({'revision': note.revision},
                                      response.data)
        self.assertDictContainsSubset({'doc_type': 'note'}, response.data)
        self.assertDictContainsSubset({'hike_uuid': note.hike.uuid},
                                      response.data)
        self.assertDictContainsSubset({'text': note.text}, response.data)
        self.assertDictContainsSubset({'date': note.date}, response.data)

    def test_delete_not_found(self):
        url = reverse('delete_document', args=['dummy'])
        self.client.delete(url, status=HTTP_404_NOT_FOUND)

    def test_delete_hike(self):
        hike = HikeFactory.create()
        url = reverse('delete_document', args=[hike.uuid])
        self.client.delete(url, status=HTTP_200_OK)

    def test_delete_note(self):
        note = NoteFactory.create()
        url = reverse('delete_document', args=[note.uuid])
        self.client.delete(url, status=HTTP_200_OK)
