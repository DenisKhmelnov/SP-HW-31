import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad
from users.models import User
from ads.serializers import *


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by("-price")
    default_serializer = AdSerializer
    serializer_classes = {
        "list": AdListSerializer,
        "retrieve": AdDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat")
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to")
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)
        return super().list(request, *args, **kwargs)

# class AdListView(ListView):
#     model = Ad
#     queryset = Ad.objects.order_by("-price")
#
#
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         paginator = Paginator(self.object_list, 4)
#         page_num = request.GET.get("page", 1)
#         page_obj = paginator.get_page(page_num)
#
#         ads = [{
#             'id': ad.pk,
#             'name': ad.name,
#             'author': ad.author.username,
#             'price': ad.price,
#             'description': ad.description,
#             'address': [loc.name for loc in ad.author.locations.all()],
#             'is_published': ad.is_published,
#                 } for ad in page_obj]
#
#         result = {
#             "items": ads,
#             "num_pages": paginator.num_pages,
#             "total": paginator.count
#         }
#
#         return JsonResponse(result, safe=False)
#
#
# class AdDetailView(DetailView):
#     model = Ad
#
#     def get(self, request, *args, **kwargs):
#         ad = self.get_object()
#         response = {
#             'id': ad.pk,
#             'name': ad.name,
#             'author': ad.author.username,
#             'price': ad.price,
#             'description': ad.description,
#             'address': [loc.name for loc in ad.author.locations.all()],
#             'is_published': ad.is_published,
#             'image': ad.image.url if ad.image else None
#         }
#
#         return JsonResponse(response)
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class AdCreateView(CreateView):
#     model = Ad
#     fields = "__all__"
#
#     def post(self, request, *args, **kwargs):
#         ad_data = json.loads(request.body)
#         author = get_object_or_404(User, pk=ad_data["author_id"])
#         category = get_object_or_404(Category, pk=ad_data["category_id"])
#         new_ad = Ad.objects.create(
#             name=ad_data["name"],
#             author=author,
#             price=ad_data["price"],
#             description=ad_data.get("description"),
#             is_published=ad_data.get("is_published", False),
#             category=category,
#         )
#
#         return JsonResponse({
#             'id': new_ad.pk,
#             'name': new_ad.name,
#             'author': new_ad.author.username,
#             'price': new_ad.price,
#             'description': new_ad.description,
#             'address': [loc.name for loc in new_ad.author.locations.all()],
#             'is_published': new_ad.is_published,
#             'image': new_ad.image.url if new_ad.image else None
#         })
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = "__all__"
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         ad_data = json.loads(request.body)
#
#         if "name" in ad_data:
#             self.object.name = ad_data["name"]
#         if "price" in ad_data:
#             self.object.price = ad_data["price"]
#         if "description" in ad_data:
#             self.object.description = ad_data["description"]
#
#         self.object.save()
#
#         return JsonResponse({
#             'id': self.object.pk,
#             'name': self.object.name,
#             'author': self.object.author.username,
#             'price': self.object.price,
#             'description': self.object.description,
#         })
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class AdUploadImage(UpdateView):
#     model = Ad
#     fields = "__all__"
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.image = request.FILES.get('image')
#         self.object.save()
#         return JsonResponse({
#             "id": self.object.pk,
#             "name": self.object.name,
#             "image": self.object.image.url
#         })
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class AdDeleteView(DeleteView):
#     model = Ad
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         ad = self.get_object()
#         ad_pk = ad.pk
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({
#             'deleted pk': ad_pk,
#         })
#
#
# # Category views
#
# class CategoryListView(ListView):
#     model = Category
#     queryset = Category.objects.order_by("name")
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         return JsonResponse([{
#             'id': cat.pk,
#             'name': cat.name,
#         } for cat in self.object_list], safe=False)
#
#
# class CategoryDetailView(DetailView):
#     model = Category
#
#     def get(self, request, *args, **kwargs):
#         request = self.get_object()
#         return JsonResponse({"id": request.pk, "name": request.name})
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class CategoryCreateView(CreateView):
#     model = Category
#     fields = "__all__"
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         new_cat = Category.objects.create(**data)
#
#         return JsonResponse({
#             'pk': new_cat.pk,
#             'name': new_cat.name,
#         })
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class CategoryUpdateView(UpdateView):
#     model = Category
#     fields = "__all__"
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#
#         data = json.loads(request.body)
#         self.object.name = data["name"]
#         self.object.save()
#
#         return JsonResponse({
#             'pk': self.object.pk,
#             'name': self.object.name,
#         })
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class CategoryDeleteView(DeleteView):
#     model = Category
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         cat = self.get_object()
#         cat_pk = cat.pk
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({
#             'deleted pk': cat_pk,
#         })
