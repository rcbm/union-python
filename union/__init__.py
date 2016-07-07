api_key = ''
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
