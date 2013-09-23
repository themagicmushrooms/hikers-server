from uuid import uuid4

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ..core.models import User


def uuid():
    return str(uuid4())


def revision():
    return "0-{0}".format(uuid())


class Document(models.Model):
    uuid = models.CharField(_('UUID'), max_length=255, default=uuid,
                            unique=True, db_index=True)
    revision = models.CharField(_('Revision'), max_length=255,
                                default=revision())
    doc_type = models.CharField(_('Document type'), max_length=255)

    def increment_revision(self):
        revision_number = int(self.revision[:self.revision.index('-')])
        self.revision = "{0}-{1}".format(revision_number + 1, uuid())

    def save(self, *args, **kwargs):
        if not self.doc_type:
            self.doc_type = self.__class__.doc_type_name()
        self.increment_revision()
        super(Document, self).save(*args, **kwargs)

    @classmethod
    def doc_type_name(cls):
        raise NotImplementedError


class Hike(Document):
    owner = models.ForeignKey(User, verbose_name=_('Owner'),
                              related_name='hikes')
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    date = models.DateTimeField(_('Date'), default=timezone.now)

    def get_absolute_url(self):
        return reverse('hike_detail', args=[self.uuid])

    def __unicode__(self):
        return u"{0}, by {1}".format(self.name, self.owner.full_name)

    @classmethod
    def doc_type_name(cls):
        return 'hike'


class Position(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return u"[{0}N,{1}E]".format(self.latitude, self.longitude)


class Note(Document):
    date = models.DateTimeField(_('Date'), default=timezone.now)
    text = models.TextField(_('Text'), null=True, blank=True)
    hike = models.ForeignKey(Hike, verbose_name=_('Hike'),
                             related_name='notes')
    position = models.OneToOneField(Position, null=True, blank=True)

    class Meta:
        ordering = ['date']

    @classmethod
    def doc_type_name(cls):
        return 'note'

    def __unicode__(self):
        return u"Note {0}, by {1}".format(self.uuid, self.hike.owner.full_name)


# TODO build this by introspection?
TYPE_TO_CLASS_MAP = {
    Hike.doc_type_name(): Hike,
    Note.doc_type_name(): Note
}
