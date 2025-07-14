import requests
from API.domain.models.product import Product
from API.ports.product_provider_port import ProductProviderPort
from typing import List
from datetime import datetime

class ProductProviderAPI(ProductProviderPort):
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url

    def get_all_products(self) -> List[Product]:
        url = f"{self.base_url}/api/v1/products"
        print(f"[DEBUG] Realizando petición a: {url}")  # ← DEBUG

        response = requests.get(url)

        print(f"[DEBUG] Código de respuesta: {response.status_code}")  # ← DEBUG

        if response.status_code != 200:
            raise Exception(f"Error al obtener productos: {response.status_code}")

        raw_data = response.json()
        #print(f"[DEBUG] Productos recibidos: {len(raw_data)}")  # ← DEBUG

        # Convertir a instancias de dominio
        return [
            Product(
                product_id=item.get("product_id"),
                name=item.get("name"),
                product_type=item.get("type"),
                farm_id=item.get("farm_id"),
                quantity=item.get("quantity"),
                price_per_unit=item.get("price_per_unit"),
                description=item.get("description"),
                harvest_date=datetime.fromisoformat(item.get("harvest_date")),
                created_at=datetime.fromisoformat(item.get("created_at")) if item.get("created_at") else None
            )
            for item in raw_data
        ]
