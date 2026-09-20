from django.urls import path

from . import views

app_name = "documents"

urlpatterns = [
    path("", views.document_list, name="list"),
    path("<int:pk>/edit/", views.document_edit, name="edit"),
    path("<int:pk>/archive-toggle/", views.document_archive_toggle, name="archive_toggle"),
]
