from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SystemSettingsForm
from .models import DEFAULTS, get_setting, set_setting


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
