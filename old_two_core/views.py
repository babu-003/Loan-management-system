from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .forms import AuditLogFilterForm, SystemSettingsForm
from .models import AuditLog, DEFAULTS, get_setting, set_setting


@login_required
def settings_edit(request):
    if request.method == "POST":
        form = SystemSettingsForm(request.POST)
        if form.is_valid():
            for key in DEFAULTS:
                set_setting(key, str(form.cleaned_data[key]))
            messages.success(request, "Settings updated.")
            return redirect("settings:edit")
    else:
        initial = {key: get_setting(key) for key in DEFAULTS}
        form = SystemSettingsForm(initial=initial)
    return render(request, "core/settings_form.html", {"form": form})


@login_required
def audit_log_list(request):
    form = AuditLogFilterForm(request.GET or None)
    logs = AuditLog.objects.select_related("actor")

    if form.is_valid():
        q = form.cleaned_data.get("q")
        entity_type = form.cleaned_data.get("entity_type")
        action = form.cleaned_data.get("action")
        date_from = form.cleaned_data.get("date_from")
        date_to = form.cleaned_data.get("date_to")
        if q:
            logs = logs.filter(entity_label__icontains=q)
        if entity_type:
            logs = logs.filter(entity_type=entity_type)
        if action:
            logs = logs.filter(action=action)
        if date_from:
            logs = logs.filter(timestamp__date__gte=date_from)
        if date_to:
            logs = logs.filter(timestamp__date__lte=date_to)

    paginator = Paginator(logs, 30)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "core/audit_log_list.html", {"page_obj": page_obj, "form": form})
