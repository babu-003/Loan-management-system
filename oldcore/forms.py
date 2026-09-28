from django import forms


class SystemSettingsForm(forms.Form):
    company_name = forms.CharField(max_length=150, required=False)
    company_address = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), required=False)
    company_phone = forms.CharField(max_length=20, required=False)
    company_email = forms.EmailField(required=False)
    currency_symbol = forms.CharField(max_length=5, required=True)
    date_format = forms.CharField(
        max_length=20, required=True,
        help_text="Python strftime format, e.g. %d-%m-%Y. Stored for future use — not yet applied to every screen.",
    )
    customer_id_prefix = forms.CharField(max_length=10, required=True)
    loan_id_prefix = forms.CharField(max_length=10, required=True)
    group_id_prefix = forms.CharField(max_length=10, required=True)
    receipt_id_prefix = forms.CharField(max_length=10, required=True)
    id_number_padding = forms.IntegerField(
        min_value=3, max_value=10, required=True,
        help_text="How many digits in the number part, e.g. 6 → CUS-000001.",
    )

    def clean_customer_id_prefix(self):
        return self.cleaned_data["customer_id_prefix"].strip().upper()

    def clean_loan_id_prefix(self):
        return self.cleaned_data["loan_id_prefix"].strip().upper()

    def clean_group_id_prefix(self):
        return self.cleaned_data["group_id_prefix"].strip().upper()

    def clean_receipt_id_prefix(self):
        return self.cleaned_data["receipt_id_prefix"].strip().upper()
