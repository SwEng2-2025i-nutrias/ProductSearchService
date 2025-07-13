from app.domain.services.product_search_service import ProductSearchService
from app.adapters.product_provider_api import ProductProviderAPI

provider = ProductProviderAPI(base_url="http://127.0.0.1:5000")
search_service = ProductSearchService(product_provider=provider)

# Ejecutar búsqueda sin filtros (debe traer todos los productos)
products = search_service.search()

print(f"Se encontraron {len(products)} productos.")
for p in products[:5]:  # solo muestra los primeros 5
    print(p.to_dict())
