import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ads.permissions import IsOwner, IsOwnerOrStaff
from ads.serializers import *


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by("-price")
    default_serializer = AdSerializer
    serializer_classes = {
        "list": AdListSerializer,
        "retrieve": AdDetailSerializer
    }

    default_permission = [AllowAny()]
    permissions = {
        "retrieve": [IsAuthenticated()],
        "update": [IsAuthenticated(), IsOwnerOrStaff()],
        "partial_update": [IsAuthenticated(), IsOwnerOrStaff()],
        "delete": [IsAuthenticated(), IsOwnerOrStaff()]
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

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


# Category views

class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by("name")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse([{
            'id': cat.pk,
            'name': cat.name,
        } for cat in self.object_list], safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        request = self.get_object()
        return JsonResponse({"id": request.pk, "name": request.name})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_cat = Category.objects.create(**data)

        return JsonResponse({
            'pk': new_cat.pk,
            'name': new_cat.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()

        return JsonResponse({
            'pk': self.object.pk,
            'name': self.object.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        cat = self.get_object()
        cat_pk = cat.pk
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'deleted pk': cat_pk,
        })


# Selection views
class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [AllowAny]


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer
    permission_classes = [IsAuthenticated]


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

# class SelectionViewSet(ModelViewSet):
#     queryset = Selection.objects.all()
#     default_serializer = SelectionSerializer
#
#     serializer_classes = {
#         "list": SelectionListSerializer,
#         "retrieve": SelectionDetailSerializer,
#     }
#
#     default_permission = [AllowAny()]
#     permissions = {
#         "retrieve": [IsAuthenticated()],
#         "create": [AllowAny()],
#         "update": [IsAuthenticated(), IsOwner()],
#         "partial_update": [IsAuthenticated(), IsOwner()],
#         "delete": [IsAuthenticated(), IsOwner()],
#     }
#
#     def get_permissions(self):
#         return self.permissions.get(self.action, self.default_permission)
#
#     def get_serializer_class(self):
#         return self.serializer_classes.get(self.action, self.default_serializer)
