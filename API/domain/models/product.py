from datetime import datetime
from typing import Optional

class Product:
    def __init__(self, 
                 product_id: Optional[int], 
                 name: str, 
                 farm_id: str,
                 type: str,
                 quantity: int,
                 price_per_unit: float,
                 description: str,
                 harvest_date: datetime,
                 created_at: Optional[datetime] = None):
        self.product_id = product_id
        self.name = name
        self.farm_id = farm_id
        self.type = type
        if quantity >= 0:
            self.quantity = quantity
        else:
            raise ValueError("Quantity cannot be negative")
        self.price_per_unit = price_per_unit
        self.description = description
        self.harvest_date = harvest_date
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "farm_id": self.farm_id,
            "type": self.type,
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "description": self.description,
            "harvest_date": self.harvest_date.isoformat() if self.harvest_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @property
    def total_value(self) -> float:
        """Calcula el valor total del producto (cantidad * precio por unidad)"""
        return self.quantity * self.price_per_unit

    def __str__(self):
        return f"Product(id={self.product_id}, name='{self.name}', type='{self.type}', quantity={self.quantity})"

    def __repr__(self):
        return self.__str__()