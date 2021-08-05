from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.fetch, name="fetch"),
    path("create/", views.create, name="create"),
    path("random/",views.random, name="random"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("?", views.search, name="search"),
]
