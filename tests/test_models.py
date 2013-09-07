
from django.test import TestCase
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from tests.factories import HikeFactory, NoteFactory
from hikers.hikes.models import Note


class NotesLocationTest(TestCase):
    def test_notes_location(self):
        """
        Tests that we can search notes by distance
        """
        hike = HikeFactory.create()
        position1 = Point(43.592157, 7.095323)
        position2 = Point(43.588535, 7.098906)
        note1 = NoteFactory.create(text=u"Lost my wallet around here", hike=hike, position=position1)
        note2 = NoteFactory.create(text=u"Discovered loss of wallet only here", hike=hike, position=position2)
        note1.save()
        note2.save()
        position3 = Point(43.586981, 7.098992)
        distance = D(m=300)
        proximal_notes = Note.objects.filter(position__distance_lte=(position3, distance))
        self.assertEqual(len(proximal_notes), 1)
