from datetime import date, timedelta
from django.core.management.base import BaseCommand
from InvoiceApp.models import Client, Invoice, InvoiceItem


DEMO = [
    ("Jean Dupont", "+237 677 12 34 56", "jean.dupont@example.com", [
        ("Ordinateur HP EliteBook 840", 2, 350_000),
        ("Imprimante Canon LBP6030", 1, 120_000),
    ]),
    ("Marie Ngo", "+237 655 98 76 54", "marie.ngo@example.com", [
        ("Écran Dell 24 pouces", 3, 95_000),
        ("Clavier mécanique Logitech", 5, 25_000),
        ("Souris sans fil", 5, 15_000),
    ]),
    ("Boutique Le Palmier", "+237 699 45 67 89", "", [
        ("Caisse enregistreuse tactile", 1, 450_000),
        ("Scanner code-barres", 2, 85_000),
    ]),
]


class Command(BaseCommand):
    help = "Crée des factures de démonstration réalistes"

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help="Supprime toutes les données avant de seeder"
        )

    def handle(self, *args, **options):
        if options['reset']:
            InvoiceItem.objects.all().delete()
            Invoice.objects.all().delete()
            Client.objects.all().delete()
            self.stdout.write(self.style.WARNING("Données existantes supprimées."))

        if Invoice.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Des factures existent déjà. Utilise --reset pour repartir de zéro."
            ))
            return

        for name, phone, email, items in DEMO:
            client = Client.objects.create(name=name, phone=phone, email=email)
            inv = Invoice.objects.create(
                client=client,
                issue_date=date.today() - timedelta(days=3),
            )
            for desc, qty, price in items:
                InvoiceItem.objects.create(
                    invoice=inv, description=desc, quantity=qty, unit_price=price
                )
            inv.recalculate_total()
            inv.save(update_fields=['total'])
            self.stdout.write(f"  ✅ {inv.number} — {client.name} — {inv.total:,} FCFA".replace(",", " "))

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ {len(DEMO)} factures de démo créées avec succès."
        ))
