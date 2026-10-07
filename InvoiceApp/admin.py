from django.contrib import admin
from .models import Client, Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ('description', 'quantity', 'unit_price')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'issue_date', 'total', 'status')
    list_filter = ('status', 'issue_date')
    search_fields = ('client__name', 'id')
    inlines = [InvoiceItemInline]
    readonly_fields = ('total',)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.recalculate_total()
        form.instance.save(update_fields=['total'])


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')