from django.core.urlresolvers import reverse

from rest_framework.status import (HTTP_200_OK, HTTP_404_NOT_FOUND,
                                   HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST,
                                   HTTP_409_CONFLICT, HTTP_204_NO_CONTENT)
from rest_framework.test import APITestCase

from tests.factories import HikeFactory, NoteFactory, UserFactory


class NonGenericAPITestNotAuthenticated(APITestCase):
    def test_get_hikes_not_authenticated(self):
        url = reverse('hike-list')
        self.client.get(url, status=HTTP_401_UNAUTHORIZED)

    def test_get_notes_not_authenticated(self):
        url = reverse('note-list')
        self.client.get(url, status=HTTP_401_UNAUTHORIZED)

    def test_get_hike_not_found(self):
        url = reverse('hike-detail', args=['dummy'])
        self.client.get(url, status=HTTP_404_NOT_FOUND)

    def test_get_hike_not_authenticated(self):
        hike = HikeFactory.create()
        url = reverse('hike-detail', args=[hike.uuid])
        self.client.get(url, status=HTTP_401_UNAUTHORIZED)

    def test_get_note_not_found(self):
        url = reverse('note-detail', args=['dummy'])
        self.client.get(url, status=HTTP_404_NOT_FOUND)

    def test_get_note_not_authenticated(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        self.client.get(url, status=HTTP_401_UNAUTHORIZED)

    def test_delete_hike_not_found(self):
        url = reverse('hike-detail', args=['dummy'])
        self.client.delete(url, status=HTTP_404_NOT_FOUND)

    def test_delete_hike_not_authenticated(self):
        hike = HikeFactory.create()
        url = reverse('hike-detail', args=[hike.uuid])
        self.client.delete(url, status=HTTP_401_UNAUTHORIZED)

    def test_delete_note_not_found(self):
        url = reverse('note-detail', args=['dummy'])
        self.client.delete(url, status=HTTP_404_NOT_FOUND)

    def test_delete_note_not_authenticated(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        self.client.delete(url, status=HTTP_401_UNAUTHORIZED)


class NonGenericAPITestAuthenticated(APITestCase):
    def test_get_hikes_not_authenticated(self):
        user1 = UserFactory.create()
        hike1 = HikeFactory.create(owner=user1)

        user2 = UserFactory.create()
        hike2 = HikeFactory.create(owner=user2)

        url = reverse('hike-list')
        self.client.force_authenticate(user=user1)
        response = self.client.get(url, status=HTTP_200_OK)
        self.assertContains(response, hike1.uuid)
        self.assertNotContains(response, hike2.uuid)

    def test_get_notes_not_authenticated(self):
        user1 = UserFactory.create()
        hike1 = HikeFactory.create(owner=user1)
        note1 = NoteFactory.create(hike=hike1)

        user2 = UserFactory.create()
        hike2 = HikeFactory.create(owner=user2)
        note2 = NoteFactory.create(hike=hike2)

        url = reverse('note-list')
        self.client.force_authenticate(user=user1)
        response = self.client.get(url, status=HTTP_200_OK)
        self.assertContains(response, note1.uuid)
        self.assertNotContains(response, note2.uuid)

    def test_get_hike(self):
        hike = HikeFactory.create()
        url = reverse('hike-detail', args=[hike.uuid])
        self.client.force_authenticate(user=hike.owner)
        response = self.client.get(url, status=HTTP_200_OK)
        self.client.logout()
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
        url = reverse('note-detail', args=[note.uuid])
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.get(url, status=HTTP_200_OK)
        self.assertDictContainsSubset({'uuid': note.uuid}, response.data)
        self.assertDictContainsSubset({'revision': note.revision},
                                      response.data)
        self.assertDictContainsSubset({'doc_type': 'note'}, response.data)
        self.assertDictContainsSubset({'hike_uuid': note.hike.uuid},
                                      response.data)
        self.assertDictContainsSubset({'text': note.text}, response.data)
        self.assertDictContainsSubset({'date': note.date}, response.data)

    def test_delete_hike_no_revision(self):
        hike = HikeFactory.create()
        self.client.force_authenticate(user=hike.owner)
        url = reverse('hike-detail', args=[hike.uuid])
        self.client.delete(url, status=HTTP_400_BAD_REQUEST)

    def test_delete_note_no_revision(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.hike.owner)
        url = reverse('note-detail', args=[note.uuid])
        self.client.delete(url + "?revision=dummy",
                           status=HTTP_400_BAD_REQUEST)

    def test_delete_hike_invalid_revision(self):
        hike = HikeFactory.create()
        self.client.force_authenticate(user=hike.owner)
        url = reverse('hike-detail', args=[hike.uuid])
        self.client.delete(url + "?revision=dummy", status=HTTP_409_CONFLICT)

    def test_delete_note_invalid_revision(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.hike.owner)
        url = reverse('note-detail', args=[note.uuid])
        self.client.delete(url + "?revision=dummy",
                           status=HTTP_400_BAD_REQUEST)

    def test_delete_hike(self):
        hike = HikeFactory.create()
        self.client.force_authenticate(user=hike.owner)
        url = reverse('hike-detail', args=[hike.uuid])
        self.client.delete(url + "?revision={0}".format(hike.revision),
                           status=HTTP_204_NO_CONTENT)

    def test_delete_note(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.hike.owner)
        url = reverse('note-detail', args=[note.uuid])
        self.client.delete(url + "?revision={0}".format(note.revision),
                           status=HTTP_204_NO_CONTENT)
