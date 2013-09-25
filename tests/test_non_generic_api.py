from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories import HikeFactory, NoteFactory, UserFactory

from hikers.hikes.models import Hike, Note


class NonGenericAPITestNotAuthenticated(APITestCase):
    def test_get_hikes_not_authenticated(self):
        url = reverse('hike-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_notes_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_hike_not_authenticated(self):
        hike = HikeFactory.create()
        url = reverse('hike-detail', args=[hike.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_note_not_authenticated(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hike_not_authenticated(self):
        hike = HikeFactory.create()
        url = reverse('hike-detail', args=[hike.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_note_not_authenticated(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_hike_not_authenticated(self):
        url = reverse('hike-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_note_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_hike_not_authenticated(self):
        url = reverse('hike-list')
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_note_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NonGenericAPITestAuthenticated(APITestCase):
    def test_get_hike_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('hike-detail', args=['dummy'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-detail', args=['dummy'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_hike_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('hike-detail', args=['dummy'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-detail', args=['dummy'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_hike_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('hike-list', args=['dummy'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-list', args=['dummy'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_hike_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('hike-list', args=['dummy'])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-list', args=['dummy'])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_hikes_not_authenticated(self):
        user1 = UserFactory.create()
        hike1 = HikeFactory.create(owner=user1)

        user2 = UserFactory.create()
        hike2 = HikeFactory.create(owner=user2)

        url = reverse('hike-list')
        self.client.force_authenticate(user=user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, note1.uuid)
        self.assertNotContains(response, note2.uuid)

    def test_get_hike(self):
        hike = HikeFactory.create()
        url = reverse('hike-detail', args=[hike.uuid])
        self.client.force_authenticate(user=hike.owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({'uuid': note.uuid}, response.data)
        self.assertDictContainsSubset({'revision': note.revision},
                                      response.data)
        self.assertDictContainsSubset({'doc_type': 'note'}, response.data)
        self.assertDictContainsSubset({'hike': note.hike.uuid},
                                      response.data)
        self.assertDictContainsSubset({'text': note.text}, response.data)
        self.assertDictContainsSubset({'date': note.date}, response.data)

    def test_delete_hike_no_revision(self):
        hike = HikeFactory.create()
        self.client.force_authenticate(user=hike.owner)
        url = reverse('hike-detail', args=[hike.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_note_no_revision(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.hike.owner)
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_hike_invalid_revision(self):
        hike = HikeFactory.create()
        self.client.force_authenticate(user=hike.owner)
        url = reverse('hike-detail', args=[hike.uuid])
        response = self.client.delete(url + "?revision=dummy")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        expected_response_data = {
            "error": ("Conflict, you are trying to delete an old revision "
                      "of this object")}
        self.assertDictContainsSubset(expected_response_data, response.data)

    def test_delete_note_invalid_revision(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.hike.owner)
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.delete(url + "?revision=dummy")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        expected_response_data = {
            "error": ("Conflict, you are trying to delete an old revision "
                      "of this object")
        }
        self.assertDictContainsSubset(expected_response_data, response.data)

    def test_delete_hike(self):
        hike = HikeFactory.create()
        self.client.force_authenticate(user=hike.owner)
        url = reverse('hike-detail', args=[hike.uuid])
        response = self.client.delete(url + "?revision={0}".format(
            hike.revision))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_note(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.hike.owner)
        url = reverse('note-detail', args=[note.uuid])
        response = self.client.delete(url + "?revision={0}".format(
            note.revision))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_new_hike(self):
        user = UserFactory.create()
        url = reverse('hike-list')
        data = {
            "uuid": "fe83cdb8-f060-4c38-9b5f-b5092a18d8cb",
            "doc_type": "hike",
            "name": "Point des Cerces",
            "date": "2013-09-10T19:11:58Z",
            "owner": user.email
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        hike = Hike.objects.get(uuid=data['uuid'])
        self.assertEqual(hike.name, data['name'])
        self.assertIsNotNone(hike.date)
        self.assertEqual(hike.owner, user)

    def test_put_hike(self):
        hike = HikeFactory.create()
        url = reverse('hike-detail', args=[hike.uuid])
        data = {
            "uuid": hike.uuid,
            "revision": hike.revision,
            "doc_type": "hike",
            "name": "New name",
            "date": "2013-09-10T19:11:58Z",
            "owner": hike.owner.email
        }
        self.client.force_authenticate(user=hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        hike = Hike.objects.get(uuid=data['uuid'])
        self.assertEqual(hike.name, data['name'])
        self.assertIsNotNone(hike.date)

    def test_put_hike_invalid_revision(self):
        hike = HikeFactory.create()
        url = reverse('hike-detail', args=[hike.uuid])
        data = {
            "uuid": hike.uuid,
            "revision": "invalid",
            "doc_type": "hike",
            "name": "New name",
            "date": "2013-09-10T19:11:58Z",
            "owner": hike.owner.email
        }
        self.client.force_authenticate(user=hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        expected_response_data = {
            "error": ("Conflict, you are trying to update an old revision "
                      "of this object")
        }
        self.assertDictContainsSubset(expected_response_data, response.data)

    def test_post_new_note(self):
        hike = HikeFactory.create()
        url = reverse('note-list')
        data = {
            "uuid": "06e35afa-36fb-46cd-bd80-dce6560e3b7b",
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972,
                "longitude": 6.1633300835308615
            },
            "hike": hike.uuid
        }
        self.client.force_authenticate(user=hike.owner)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(uuid=data['uuid'])
        self.assertEqual(note.text, data['text'])
        self.assertIsNotNone(note.date)
        self.assertEqual(note.hike, hike)
        self.assertTrue(abs(note.position.latitude - data['position']['latitude'])
                        < 0.001)
        self.assertTrue(abs(note.position.longitude - data['position']['longitude'])
                        < 0.001)

    def test_post_note_no_hike(self):
        hike = HikeFactory.create()
        url = reverse('note-list')
        data = {
            "uuid": "06e35afa-36fb-46cd-bd80-dce6560e3b7b",
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972,
                "longitude": 6.1633300835308615
            }
        }
        self.client.force_authenticate(user=hike.owner)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972,
                "longitude": 6.16333008353723
            },
            "hike": note.hike.uuid
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = Note.objects.get(uuid=data['uuid'])
        self.assertEqual(note.text, data['text'])
        self.assertIsNotNone(note.date)
        self.assertEqual(note.hike.uuid, data['hike'])
        self.assertTrue(abs(note.position.latitude - data['position']['latitude'])
                        < 0.001)
        self.assertTrue(abs(note.position.longitude - data['position']['longitude'])
                        < 0.001)

    def test_put_note_no_revision(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972,
                "longitude": 6.1633300835308615
            },
            "hike": note.hike.uuid
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_invalid_revision(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": "invalid",
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972,
                "longitude": 6.1633300835308615
            },
            "hike": note.hike.uuid
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        expected_response_data = {
            "error": ("Conflict, you are trying to update an old revision "
                      "of this object")
        }
        self.assertDictContainsSubset(expected_response_data, response.data)

    def test_put_note_no_hike(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972,
                "longitude": 6.1633300835308615
            }
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_invalid_hike(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972,
                "longitude": 6.1633300835308615
            },
            "hike": "dummy"
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_no_position(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "hike": note.hike.uuid
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_invalid_position(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "hike": note.hike.uuid,
            "position": "test"
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_invalid_latitude(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": "test",
                "longitude": 6.1633300835308615
            },
            "hike": note.hike.uuid
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_missing_latitude(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "longitude": 6.1633300835308615
            },
            "hike": note.hike.uuid
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_invalid_longitude(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972,
                "longitude": "test"
            },
            "hike": note.hike.uuid
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_note_missing_longitude(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.uuid])
        data = {
            "uuid": note.uuid,
            "revision": note.revision,
            "doc_type": "note",
            "date": "2013-09-10T20:33:40Z",
            "text": "Test",
            "position": {
                "latitude": 46.20934846967972
            },
            "hike": note.hike.uuid
        }
        self.client.force_authenticate(user=note.hike.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
