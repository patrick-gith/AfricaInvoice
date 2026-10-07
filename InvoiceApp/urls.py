from django.urls import path
from . import views

app_name = 'InvoiceApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('invoices/new/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('invoices/<int:pk>/toggle/', views.invoice_toggle_status, name='invoice_toggle'),
    path('invoices/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
]