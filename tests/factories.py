from factory import Factory, lazy_attribute, Sequence
from factory.declarations import SubFactory

from hikers.core.models import User
from hikers.hikes.models import Hike, Note


class UserFactory(Factory):
    FACTORY_FOR = User
    email = Sequence(lambda n: 'the_brain{0}@acme.com'.format(n))

    @lazy_attribute
    def full_name(self):
        return "The Brain"

    @lazy_attribute
    def password(self):
        return "123"

    @lazy_attribute
    def is_active(self):
        return True

    @classmethod
    def _prepare(cls, create, **kwargs):
        if create:
            return User.objects.create_user(**kwargs)
        else:
            return super(UserFactory, cls)._prepare(create, **kwargs)


class HikeFactory(Factory):
    FACTORY_FOR = Hike
    owner = SubFactory(UserFactory)

    @lazy_attribute
    def name(self):
        return "Pointe des Cerces"


class NoteFactory(Factory):
    FACTORY_FOR = Note
    hike = SubFactory(HikeFactory)

    @lazy_attribute
    def text(self):
        return "Almost no snow."

    @lazy_attribute
    def position(self):
        return "POINT(2.0 45.0)"
