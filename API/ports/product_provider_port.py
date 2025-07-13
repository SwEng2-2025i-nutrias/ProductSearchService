from abc import ABC, abstractmethod
from typing import List
from API.domain.models.product import Product

class ProductProviderPort(ABC):
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass
