import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from ads.models import Categories, Ads


def get(request):
    return JsonResponse({
        "status": "ok"
    })


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        request = self.get_object()
        return JsonResponse({"id": request.pk, "name": request.name})


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        request = self.get_object()
        response = {
            'id': request.pk,
            'name': request.name,
            'author': request.author,
            'price': request.price,
            'description': request.description,
            'address': request.address,
            'is_published': request.is_published,
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class AdsListCreateView(View):
    def get(self, request):
        ads_list = Ads.objects.all()

        return JsonResponse([{
            'id': ad.pk,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published,
        } for ad in ads_list], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ads.objects.create(**data)

        return JsonResponse({
            'id': new_ad.pk,
            'name': new_ad.name,
            'author': new_ad.author,
            'price': new_ad.price,
            'description': new_ad.description,
            'address': new_ad.address,
            'is_published': new_ad.is_published,
        } )


@method_decorator(csrf_exempt, name="dispatch")
class CatListCreateView(View):
    def get(self, request):
        cat_list = Ads.objects.all()

        return JsonResponse([{
            'pk': cat.pk,
            'name': cat.name,
        } for cat in cat_list], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_cat = Categories.objects.create(**data)

        return JsonResponse({
            'pk': new_cat.pk,
            'name': new_cat.name,
        })
