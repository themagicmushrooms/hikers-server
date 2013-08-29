from django.core.urlresolvers import reverse

from django_webtest import WebTest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from tests.factories import HikeFactory, NoteFactory


class HikesTest(WebTest):
    def test_my_hikes(self):
        url = reverse('my_hikes')
        response = self.app.get(url)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

        name = 'Grande Casse'
        hike = HikeFactory.create(name=name)
        response = self.app.get(url, user=hike.owner.email)
        self.assertContains(response, name)
        self.assertContains(response, hike.get_absolute_url())

    def test_hike_detail(self):
        name = 'Grande Casse'
        hike = HikeFactory.create(name=name)
        note = NoteFactory.create(text=u"Marmots!", hike=hike)
        url = reverse('hike_detail', args=[hike.uuid])
        response = self.app.get(url)
        self.assertNotEqual(response.status_code, HTTP_200_OK)

        response = self.app.get(url, user=hike.owner.email)
        self.assertContains(response, hike.name)
        self.assertContains(response, note.text)

        url = reverse('hike_detail', args=['dummy'])
        self.app.get(url, user=hike.owner.email, status=HTTP_404_NOT_FOUND)
