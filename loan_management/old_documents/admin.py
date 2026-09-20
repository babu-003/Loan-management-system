from django.contrib import admin

from .models import CustomerDocument, DocumentType


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "scope", "is_active", "display_order")
    list_filter = ("scope", "is_active")
    ordering = ("scope", "display_order")


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ("customer", "document_type", "document_number", "verified_status", "is_archived", "uploaded_date")
    list_filter = ("verified_status", "document_type", "is_archived")
    search_fields = ("customer__customer_id", "customer__full_name", "document_number")
