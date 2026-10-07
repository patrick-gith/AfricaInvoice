import base64
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML


def _load_logo_data_url():
    """Charge assets/logo.png et le retourne en data URL base64."""
    logo_path = Path(settings.BASE_DIR) / 'assets' / 'logo.png'

    print(f"[PDF] Recherche logo : {logo_path}")

    if not logo_path.exists():
        print(f"[PDF] ❌ Logo introuvable à {logo_path}")
        return None

    try:
        raw = logo_path.read_bytes()
        b64 = base64.b64encode(raw).decode('ascii')
        print(f"[PDF] ✅ Logo chargé ({len(raw)} octets → {len(b64)} b64)")
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        print(f"[PDF] ❌ Erreur lecture logo : {e}")
        return None


def render_invoice_pdf(invoice, company):
    logo_data_url = _load_logo_data_url()

    html_string = render_to_string(
        'dashboard/invoice_pdf.html',
        {
            'invoice': invoice,
            'client': invoice.client,
            'items': invoice.items.all(),
            'company': company,
            'logo_data_url': logo_data_url,
        },
    )

    return HTML(string=html_string).write_pdf()