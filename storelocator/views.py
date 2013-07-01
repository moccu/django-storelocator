from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic.base import View
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.utils import translation

from .forms import StoreLocatorForm
from .models import Location, StoreLocator
from .utils import get_near_shops

import json


class ExtendedEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'serialize'):
            return obj.serialize()
        elif isinstance(obj, QuerySet):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class StoreLocatorView(FormMixin, View):
    """
    A view for processing a form with json response
    """

    form_class = StoreLocatorForm

    @method_decorator(cache_page(60 * 60))
    def dispatch(self, request, slug, *args, **kwargs):
        self.storelocator = get_object_or_404(StoreLocator, slug=slug)
        self.callback = request.GET.get('callback')
        self.language = request.GET.get('language')

        if self.language:
            translation.activate(self.language)
            request.LANGUAGE_CODE = translation.get_language()

        return super(StoreLocatorView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        return {'data': self.request.GET}

    def form_valid(self, form):
        result_limit = form.limit_max
        filter_radius = form.radius_max

        context = self.get_json_context(form)

        latitude = form.cleaned_data.get('latitude')
        longitude = form.cleaned_data.get('longitude')
        postalcode = form.cleaned_data.get('postalcode')
        iso = form.cleaned_data.get('iso')
        limit = form.cleaned_data.get('limit')
        radius = form.cleaned_data.get('radius')

        if limit == 0:
            result_limit = limit

        if limit:
            result_limit = limit

        if radius:
            filter_radius = radius

        if latitude and longitude:
            context['shops'] = get_near_shops(
                self.storelocator,
                latitude,
                longitude,
                result_limit,
                filter_radius,
                True,
                iso=None)

        if postalcode:
            locations = Location.objects.filter(postalcode=postalcode)

            if locations:
                location = locations[0]
                context['shops'] = get_near_shops(
                    self.storelocator,
                    location.latitude,
                    location.longitude,
                    result_limit,
                    filter_radius,
                    False,
                    iso)

        return self.json_response(context)

    def form_invalid(self, form):
        context = self.get_json_context(form)
        return self.json_response(context)

    def get_json_context(self, form):
        errors = form.errors.copy()
        if errors.get('__all__'):
            del errors['__all__']

        context = {
            'success': form.is_valid(),
            'form_errors': errors,
            'non_field_errors': form.non_field_errors(),
            'shops': [],
        }
        return context

    def json_response(self, context):
        serialized = json.dumps(context, cls=ExtendedEncoder)

        if self.callback:
            serialized = "%s(%s)" % (self.callback, serialized)

        return HttpResponse(serialized, mimetype='application/json')
