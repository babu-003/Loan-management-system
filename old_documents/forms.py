from django import forms

from .models import CustomerDocument, DocumentType


class DocumentEditForm(forms.ModelForm):
    """Corrects an existing document row (wrong number, replace a bad
    scan). Verification status is deliberately NOT editable here — that
    stays a separate action (see verify_customer_document in the
    customers app) so the two workflows never fight over the same field.
    """

    class Meta:
        model = CustomerDocument
        fields = ["document_type", "document_number", "file", "remarks"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["document_type"].queryset = DocumentType.objects.filter(
            scope=DocumentType.SCOPE_CUSTOMER, is_active=True
        )

    def clean(self):
        cleaned_data = super().clean()
        document_number = cleaned_data.get("document_number")
        # `file` may be an already-saved FieldFile even if nothing new is
        # uploaded this time, so check the instance's existing file too.
        has_file = bool(cleaned_data.get("file")) or bool(self.instance.file)
        if not document_number and not has_file:
            raise forms.ValidationError(
                "Provide either an uploaded file or a document/ID number."
            )
        return cleaned_data


class DocumentManagementSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search (Customer ID / Name / Doc. Number)")
    document_type = forms.ModelChoiceField(
        required=False,
        queryset=DocumentType.objects.filter(scope=DocumentType.SCOPE_CUSTOMER),
    )
    verified_status = forms.ChoiceField(
        required=False,
        choices=[("", "All statuses")] + list(CustomerDocument.STATUS_CHOICES),
    )
    show_archived = forms.BooleanField(required=False, label="Show archived only")
