import os
from datetime import datetime
from flask import Blueprint, request, jsonify

from API.use_cases.search_use_cases import SearchProductsUseCase
from API.adapters.product_provider_api import ProductProviderAPI
from API.domain.services.product_search_service import ProductSearchService

# Blueprint de búsqueda de productos
product_search_bp = Blueprint(
    "product_search_bp", __name__, url_prefix="/api/v1"
)

# Inicialización del servicio de búsqueda - Importante, este el es puerto de  ProductServiceAPI
provider = ProductProviderAPI("http://127.0.0.1:5000")
search_service = ProductSearchService(product_provider=provider)
use_case = SearchProductsUseCase(product_search_service=search_service)


def parse_date(date_str: str):
    try:
        return datetime.fromisoformat(date_str) if date_str else None
    except ValueError:
        return None


@product_search_bp.route("/product-search", methods=["GET"])
def search_products():
    """
    Buscar productos con múltiples filtros y ordenamiento.
    ---
    tags:
      - Product Search
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: Nombre parcial o completo
      - name: min_price
        in: query
        type: number
        format: float
        required: false
      - name: max_price
        in: query
        type: number
        format: float
        required: false
      - name: min_quantity
        in: query
        type: integer
        required: false
      - name: max_quantity
        in: query
        type: integer
        required: false
      - name: harvest_start
        in: query
        type: string
        format: date
        required: false
        description: Fecha mínima de cosecha (YYYY-MM-DD)
      - name: harvest_end
        in: query
        type: string
        format: date
        required: false
    responses:
      200:
        description: Lista de productos filtrados
        schema:
          type: array
          items:
            type: object
            properties:
              product_id:
                type: integer
              name:
                type: string
              farm_id:
                type: string
              type:
                type: string
              quantity:
                type: integer
              price_per_unit:
                type: number
              description:
                type: string
              harvest_date:
                type: string
                format: date-time
              created_at:
                type: string
                format: date-time
    """
    # Extracción de parámetros
    args = request.args

    products = use_case.execute(
        name=args.get("name"),
        min_price=float(args.get("min_price")) if args.get("min_price") else None,
        max_price=float(args.get("max_price")) if args.get("max_price") else None,
        min_quantity=int(args.get("min_quantity")) if args.get("min_quantity") else None,
        max_quantity=int(args.get("max_quantity")) if args.get("max_quantity") else None,
        harvest_date_start=parse_date(args.get("harvest_start")),
        harvest_date_end=parse_date(args.get("harvest_end")),
        order_by=args.get("order_by"),
        order_dir=args.get("order_dir", "asc")
    )

    return jsonify([p.to_dict() for p in products]), 200
