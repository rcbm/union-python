api_key = '0a3a9b8fbd1fc460104040eb548d941d'
api_namespace = 'api'
api_version = "v1"
# host = "api.unionbilling.com"
host = "api.union.dev"
protocol = "http"

# Union Models
from union.models import (
    Customer,
    BaseModel
)

# API Client
from union.client import UnionClient

# Union models
MODEL_MAP = [
        {'model': Customer, 'name': 'customer', 'plural': 'customers'},
]
