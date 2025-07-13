from typing import List, Optional
from datetime import datetime
from API.domain.models.product import Product
from API.domain.services.product_search_service import ProductSearchService

class SearchProductsUseCase:


    def __init__(self, product_search_service: ProductSearchService):
        self.product_search_service = product_search_service

    def execute(self,
                name: Optional[str] = None,
                min_price: Optional[float] = None,
                max_price: Optional[float] = None,
                min_quantity: Optional[int] = None,
                max_quantity: Optional[int] = None,
                harvest_date_start: Optional[datetime] = None,
                harvest_date_end: Optional[datetime] = None,
                order_by: Optional[str] = None,
                order_dir: str = "asc") -> List[Product]:
        """
        Ejecuta la búsqueda con filtros combinados y ordenamiento.
        """

        # Filtrar productos
        filtered = self.product_search_service.search(
            name=name,
            min_price=min_price,
            max_price=max_price,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
            harvest_date_start=harvest_date_start,
            harvest_date_end=harvest_date_end,
        )

        # Ordenar si se requiere
        if order_by:
            filtered = self.product_search_service.sort_products(
                products=filtered,
                order_by=order_by,
                order_dir=order_dir,
            )

        return filtered
