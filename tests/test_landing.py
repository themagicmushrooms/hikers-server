from django.core.urlresolvers import reverse

from django_webtest import WebTest


class LandingTest(WebTest):
    def test_landing(self):
        url = reverse('landing')
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hikers')
