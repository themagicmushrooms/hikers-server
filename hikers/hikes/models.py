from uuid import uuid4

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ..core.models import User


def uuid():
    return str(uuid4())


class Hike(models.Model):
    uuid = models.CharField(_('uuid'), max_length=255, default=uuid,
                            unique=True, db_index=True)
    owner = models.ForeignKey(User, verbose_name=_('Owner'),
                              related_name='hikes')
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    date = models.DateTimeField(_('Date'), default=timezone.now)

    def get_absolute_url(self):
        return reverse('hike_detail', args=[self.uuid])

    def __unicode__(self):
        return u"{0}, by {1}".format(self.name, self.owner.full_name)


class Note(models.Model):
    uuid = models.CharField(_('uuid'), max_length=255, default=uuid,
                            unique=True, db_index=True)
    date = models.DateTimeField(_('Date'), default=timezone.now)
    text = models.TextField(_('Text'), null=True, blank=True)
    hike = models.ForeignKey(Hike, verbose_name=_('Hike'),
                             related_name='notes')

    class Meta:
        ordering = ['date']
