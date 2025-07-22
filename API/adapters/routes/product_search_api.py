import time
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from API.use_cases.search_use_cases import SearchProductsUseCase
from API.adapters.product_provider_api import ProductProviderAPI
from API.domain.services.product_search_service import ProductSearchService

product_search_bp = Blueprint("product_search_bp", __name__, url_prefix="/api/v1")

# --- Métricas de Prometheus ---
REQUEST_COUNT = Counter(
    'product_filter_requests_total',
    'Total de solicitudes al endpoint de filtrado',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'product_filter_request_latency_seconds',
    'Latencia de las solicitudes al endpoint de filtrado',
    ['endpoint']
)

FILTER_USAGE = Counter(
    'product_search_filter_usage_total',
    'Veces que se ha aplicado cada filtro en la búsqueda de productos',
    ['filter']
)

@product_search_bp.before_request
def before_request():
    # Inicia el timer (context manager) y lo guardamos en request
    request._prom_timer = REQUEST_LATENCY.labels(endpoint=request.path).time()

@product_search_bp.after_request
def after_request(response):
    # 1) contador de peticiones
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code
    ).inc()

    # 2) calcula latencia y observa
    latency = time.time() - getattr(request, "_start_time", time.time())
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)

    # 3) contador de filtros
    for filtro in (
        'name','type','min_price','max_price',
        'min_quantity','max_quantity',
        'harvest_start','harvest_end',
        'order_by','order_dir'
    ):
        if request.args.get(filtro) is not None:
            FILTER_USAGE.labels(filter=filtro).inc()

    return response
# Añadimos /metrics aquí si quieres exponerlas también bajo /api/v1/metrics
@product_search_bp.route("/metrics", methods=["GET"])
def metrics_bp():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# --- Resto de tu código de rutas ---
provider = ProductProviderAPI(
    os.getenv("PRODUCT_SERVICE_URL", "http://127.0.0.1:5000")
)
search_service = ProductSearchService(product_provider=provider)
use_case = SearchProductsUseCase(product_search_service=search_service)

def parse_date(date_str: str):
    try:
        return datetime.fromisoformat(date_str).date() if date_str else None
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
      - name: type
        in: query
        type: string
        required: false
        description: Tipo de producto
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
        description: Fecha máxima de cosecha (YYYY-MM-DD)
      - name: order_by
        in: query
        type: string
        required: false
        description: Campo para ordenar (name, price_per_unit, quantity, harvest_date)
      - name: order_dir
        in: query
        type: string
        required: false
        description: Dirección de orden (asc o desc)
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
                format: date
              created_at:
                type: string
                format: date-time
        examples:
          application/json:
            - product_id: 1
              name: "Maíz amarillo"
              farm_id: "FARM001"
              type: "Grano"
              quantity: 100
              price_per_unit: 25.5
              description: "Maíz de alta calidad"
              harvest_date: "2025-06-01T00:00:00"
              created_at: "2025-06-10T12:00:00"
      500:
        description: Error interno del servidor
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error detallado
        examples:
          application/json:
            error: "Ocurrió un error interno al procesar la solicitud"
    """
    args = request.args

    products = use_case.execute(
        name=args.get("name"),
        product_type=args.get("type"),
        min_price=float(args.get("min_price")) if args.get("min_price") else None,
        max_price=float(args.get("max_price")) if args.get("max_price") else None,
        min_quantity=int(args.get("min_quantity")) if args.get("min_quantity") else None,
        max_quantity=int(args.get("max_quantity")) if args.get("max_quantity") else None,
        harvest_date_start=parse_date(args.get("harvest_start")),
        harvest_date_end=parse_date(args.get("harvest_end")),
        order_by=args.get("order_by"),
        order_dir=args.get("order_dir", "asc")
    )

    try:
        return jsonify([p.to_dict() for p in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
