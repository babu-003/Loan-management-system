from django.db import models

# Known setting keys and their defaults. New settings can be added here
# later without any migration — SystemSetting is a plain key/value table,
# so a new key is just a new row, not a new column.
DEFAULTS = {
    "company_name": "",
    "company_address": "",
    "company_phone": "",
    "company_email": "",
    "currency_symbol": "₹",
    "date_format": "%d-%m-%Y",
    "customer_id_prefix": "CUS",
    "loan_id_prefix": "LN",
    "group_id_prefix": "GRP",
    "receipt_id_prefix": "REC",
    "id_number_padding": "6",
}


class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)

    def __str__(self):
        return self.key


def get_setting(key, default=None):
    """Reads a setting, falling back to DEFAULTS (then the given default)
    if it's never been saved yet — so the app works with zero setup and
    only writes a row once an admin actually changes something."""
    try:
        return SystemSetting.objects.get(key=key).value
    except SystemSetting.DoesNotExist:
        return DEFAULTS.get(key, default)


def set_setting(key, value):
    SystemSetting.objects.update_or_create(key=key, defaults={"value": value})
