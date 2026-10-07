from django import forms
from django.forms import inlineformset_factory
from .models import Client, Invoice, InvoiceItem


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Jean Dupont', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '+237 6 XX XX XX XX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'client@example.com'}),
        }


class InvoiceForm(forms.ModelForm):
    issue_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Invoice
        fields = ['issue_date', 'due_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Merci pour votre confiance.'}),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Ordinateur HP EliteBook'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'value': 1}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': 1, 'value': 0}),
        }


InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True,
)