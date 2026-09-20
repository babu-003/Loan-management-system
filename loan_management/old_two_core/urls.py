from django.urls import path

from . import views

app_name = "settings"

urlpatterns = [
    path("", views.settings_edit, name="edit"),
    path("audit-log/", views.audit_log_list, name="audit_log"),
]
