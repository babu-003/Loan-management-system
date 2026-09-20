from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import DocumentEditForm, DocumentManagementSearchForm
from .models import CustomerDocument


@login_required
def document_list(request):
    """Cross-customer document management: search/filter every KYC
    document in the system, not just one customer's tab. This is the
    'Documents Management' entry point."""
    search_form = DocumentManagementSearchForm(request.GET or None)
    documents = CustomerDocument.objects.select_related("customer", "document_type")

    show_archived = False
    if search_form.is_valid():
        query = search_form.cleaned_data.get("q")
        document_type = search_form.cleaned_data.get("document_type")
        verified_status = search_form.cleaned_data.get("verified_status")
        show_archived = search_form.cleaned_data.get("show_archived")

        if query:
            documents = documents.filter(
                Q(customer__customer_id__icontains=query)
                | Q(customer__full_name__icontains=query)
                | Q(document_number__icontains=query)
            )
        if document_type:
            documents = documents.filter(document_type=document_type)
        if verified_status:
            documents = documents.filter(verified_status=verified_status)

    documents = documents.filter(is_archived=show_archived)

    paginator = Paginator(documents, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "documents/document_list.html",
        {
            "page_obj": page_obj,
            "search_form": search_form,
            "show_archived": show_archived,
        },
    )


@login_required
def document_edit(request, pk):
    document = get_object_or_404(CustomerDocument, pk=pk)
    if request.method == "POST":
        form = DocumentEditForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Document updated.")
            return redirect("documents:list")
    else:
        form = DocumentEditForm(instance=document)
    return render(
        request, "documents/document_edit_form.html", {"form": form, "document": document}
    )


@login_required
def document_archive_toggle(request, pk):
    """Archives or restores a document. Archiving never deletes the row —
    it just stops counting it as active KYC, keeping the history intact."""
    document = get_object_or_404(CustomerDocument, pk=pk)
    if request.method == "POST":
        document.is_archived = not document.is_archived
        document.archived_at = timezone.now() if document.is_archived else None
        document.save(update_fields=["is_archived", "archived_at"])
        action = "archived" if document.is_archived else "restored"
        messages.success(request, f"Document {action}.")
    next_url = request.POST.get("next") or reverse("documents:list")
    return redirect(next_url)
