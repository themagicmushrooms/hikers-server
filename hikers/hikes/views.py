from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views import generic

from ..core.models import User

from .models import Hike


class HikeDetail(generic.TemplateView):
    model = Hike
    template_name = "hikes/hike_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.hike = get_object_or_404(Hike, uuid=kwargs['uuid'])
        return super(HikeDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(HikeDetail, self).get_context_data(**kwargs)
        data['hike'] = self.hike
        data['notes'] = self.hike.notes.all()
        return data
hike_detail = login_required(HikeDetail.as_view())


class MyHikes(generic.ListView):
    model = Hike
    template_name = "hikes/my_hikes.html"

    def get_queryset(self):
        self.owner = get_object_or_404(User, email=self.request.user)
        return Hike.objects.filter(owner=self.owner)
my_hikes = login_required(MyHikes.as_view())
