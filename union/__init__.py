api_key = ''
api_namespace = 'api'
api_version = "v1"
host = "api.unionbilling.com"
protocol = "http"

# Union Models
from union.models import (
    BaseModel,
    Customer,
    CustomerInvoice,
    Vendor,
    VendorInvoice,
    Sale,
    SaleItem,
)

# API Client
from union.client import UnionClient

# Union models
MODEL_MAP = [
        {'model': Customer, 'name': 'customer', 'plural': 'customers'},
        {'model': CustomerInvoice, 'name': 'customer_invoice', 'plural': 'customer_invoices'},
        {'model': Vendor, 'name': 'vendor', 'plural': 'vendors'},
        {'model': VendorInvoice, 'name': 'vendor_invoice', 'plural': 'vendor_invoices'},
        {'model': Sale, 'name': 'sale', 'plural': 'sales'},
        {'model': SaleItem, 'name': 'sale_item', 'plural': 'sale_items'},
]
