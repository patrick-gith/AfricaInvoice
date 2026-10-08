from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import Client, Invoice, InvoiceItem


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email', 'address']

        labels = {
            'name': _('Name'),
            'phone': _('Phone'),
            'email': _('Email'),
            'address': _('Address'),
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': _('John Doe'),
                    'class': 'form-input',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': '+237 6 XX XX XX XX',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'client@example.com',
                }
            ),
            'address': forms.Textarea(
                attrs={
                    'placeholder': _('Client address'),
                    'rows': 3,
                }
            ),
        }


class InvoiceForm(forms.ModelForm):
    issue_date = forms.DateField(
        label=_('Issue date'),
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )

    due_date = forms.DateField(
        label=_('Due date'),
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )

    class Meta:
        model = Invoice
        fields = ['issue_date', 'due_date', 'notes']

        labels = {
            'notes': _('Notes'),
        }

        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'rows': 2,
                    'placeholder': _('Thank you for your trust.'),
                }
            ),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']

        labels = {
            'description': _('Description'),
            'quantity': _('Quantity'),
            'unit_price': _('Unit price'),
        }

        widgets = {
            'description': forms.TextInput(
                attrs={
                    'placeholder': _(
                        'HP EliteBook laptop'
                    ),
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'min': 1,
                    'value': 1,
                }
            ),
            'unit_price': forms.NumberInput(
                attrs={
                    'min': 0,
                    'step': 1,
                    'value': 0,
                }
            ),
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
