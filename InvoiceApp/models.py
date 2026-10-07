from datetime import date
from django.db import models


class Client(models.Model):
    name = models.CharField("Nom", max_length=200)
    phone = models.CharField("Téléphone", max_length=30, blank=True)
    email = models.EmailField("Email", blank=True)
    address = models.CharField("Adresse", max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Impayée'),
        ('paid', 'Payée'),
    ]

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='invoices')
    issue_date = models.DateField("Date d'émission", default=date.today)
    due_date = models.DateField("Date d'échéance", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    notes = models.TextField("Notes", blank=True)
    total = models.PositiveBigIntegerField("Total (FCFA)", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.number

    @property
    def number(self):
        return f"INV-{self.id:04d}" if self.id else "INV-XXXX"

    def recalculate_total(self):
        self.total = sum(item.line_total for item in self.items.all())
        return self.total


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField("Produit", max_length=200)
    quantity = models.PositiveIntegerField("Quantité", default=1)
    unit_price = models.PositiveBigIntegerField("Prix unitaire (FCFA)", default=0)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} x{self.quantity}"