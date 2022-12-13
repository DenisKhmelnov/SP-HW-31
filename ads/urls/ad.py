from django.contrib import admin
from django.urls import path

from ads.views import AdsDetailView, AdsListCreateView

urlpatterns = [
    path('', AdsListCreateView.as_view()),
    path('<int:pk>', AdsDetailView.as_view()),
]