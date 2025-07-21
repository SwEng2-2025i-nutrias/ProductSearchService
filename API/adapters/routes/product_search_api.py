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
