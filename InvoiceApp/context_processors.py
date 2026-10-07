from django.conf import settings
from django.urls import reverse


def index_url_processor(request):
    return {'index_url': reverse('InvoiceApp:index')}


def company_processor(request):
    return {
        'company': {
            'name': settings.COMPANY_NAME,
            'address': settings.COMPANY_ADDRESS,
            'phone': settings.COMPANY_PHONE,
            'email': settings.COMPANY_EMAIL,
            'tax_id': settings.COMPANY_TAX_ID,
            'currency': 'FCFA',
        }
    }