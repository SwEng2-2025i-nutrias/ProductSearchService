from typing import List, Optional
from datetime import datetime
from API.domain.models.product import Product
from API.adapters.product_provider_api import ProductProviderAPI
#from API.domain.services.product_search_service import ProductSearchService

class ProductSearchService:
    def __init__(self, product_provider):
        """
        product_provider: clase o función que devuelve una lista de productos.
        Puede ser un repositorio o una API.
        """
        self.product_provider = product_provider

    def search(self,
               name: Optional[str] = None,
               min_price: Optional[float] = None,
               max_price: Optional[float] = None,
               min_quantity: Optional[int] = None,
               max_quantity: Optional[int] = None,
               #falta agregar el filtro 
               #falta agregar la fecha de cosecha 
               #
               harvest_date_start: Optional[datetime] = None,
               harvest_date_end: Optional[datetime] = None) -> List[Product]:

        products = self.product_provider.get_all_products()

        if name:
            products = [p for p in products if name.lower() in p.name.lower()]

        if min_price is not None:
            products = [p for p in products if p.price_per_unit >= min_price]

        if max_price is not None:
            products = [p for p in products if p.price_per_unit <= max_price]

        if min_quantity is not None:
            products = [p for p in products if p.quantity >= min_quantity]

        if max_quantity is not None:
            products = [p for p in products if p.quantity <= max_quantity]

        if harvest_date_start is not None:
            products = [p for p in products if p.harvest_date >= harvest_date_start]

        if harvest_date_end is not None:
            products = [p for p in products if p.harvest_date <= harvest_date_end]

        return products

    def sort_products(self,
                      products: List[Product],
                      order_by: str,
                      order_dir: str = "asc") -> List[Product]:
        
        reverse:bool = order_dir.lower() == "desc"
        valid_fields = {"name", "price_per_unit", "quantity", "harvest_date"}

        if order_by not in valid_fields:
            return products  # No ordena si no es un campo válido

        return sorted(products, key=lambda p: getattr(p, order_by), reverse=reverse)
#Falta agregar por mayor cantidad  