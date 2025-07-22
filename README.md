# 🔎 Product Search Service

**Product Search Service** es una API REST desarrollada en Python con Flask que permite realizar búsquedas avanzadas de productos agrícolas mediante múltiples filtros y ordenamientos, siguiendo principios de arquitectura hexagonal.

---

## 🚀 Tecnologías Utilizadas

- **Python 3.9+**
- **Flask 2.x** – Microframework web para Python
- **Flasgger** – Documentación Swagger/OpenAPI automática
- **SQLite** – Base de datos ligera para desarrollo
- **Requests** – Cliente HTTP para consumir `ProductService`

---

## 📁 Estructura del Proyecto

```
ProductSearchService/               # Raíz del proyecto
├── .env                           # Variables de entorno (puerto, URL de servicios)
├── main.py                        # Punto de entrada de la aplicación
├── README.md                      # Documentación (este archivo)
├── requirements.txt               # Dependencias Python
│
├── API/                           # Código principal (package)
│   ├── app/                       # Adaptadores de entrada (HTTP, CLI, etc.)
│   │   └── factory.py             # Fábrica de la app, Swagger y blueprints
│   │
│   ├── adapters/                  # Adaptadores de infraestructura
│   │   ├── routes/                # Rutas y controladores HTTP
│   │   │   └── product_search_api.py
│   │   └── product_provider_api.py# HTTP client a ProductService
│   │
│   ├── docs/                      # Specs Swagger (si se usaran .yml externos)
│   │   └── get_product_search.yml
│   │
│   ├── ports/                     # Puertos (interfaces) de salida
│   │   └── product_provider_port.py
│   │
│   ├── domain/                    # Lógica de negocio
│   │   ├── models/                # Entidades del dominio
│   │   │   └── product.py
│   │   └── services/              # Reglas de búsqueda y ordenamiento
│   │       └── product_search_service.py
│   │
│   └── use_cases/                 # Casos de uso (application layer)
│       └── search_use_cases.py
│
└── tests/                         # Pruebas unitarias e integración
    └── test_product_search.py
```

---

## ⚡ Instalación y Ejecución

1. **Clonar el repositorio**

   ```bash
   git clone <url-repo>
   cd ProductSearchService
   ```

2. **Crear entorno virtual y activar**

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux/macOS
   .\.venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**

   - Copiar `.env.example` a `.env` y ajustar:

     ```ini
     PORT=5002
     PRODUCT_SERVICE_URL=http://127.0.0.1:5000
     FLASK_DEBUG=False
     ```

5. **Ejecutar la aplicación**

   ```bash
   python main.py
   ```

   - La API quedará expuesta en `http://127.0.0.1:5002`
   - Swagger UI disponible en `http://127.0.0.1:5002/swagger/`

---

## 📡 Endpoints

### Buscar Productos

```http
GET /api/v1/product-search
```

#### Query Parameters

| Parámetro       | Tipo    | Descripción                                                              |
| --------------- | ------- | ------------------------------------------------------------------------ |
| `name`          | string  | Búsqueda parcial por nombre                                              |
| `min_price`     | number  | Precio mínimo                                                            |
| `max_price`     | number  | Precio máximo                                                            |
| `min_quantity`  | integer | Cantidad mínima                                                          |
| `max_quantity`  | integer | Cantidad máxima                                                          |
| `harvest_start` | date    | Fecha de cosecha mínima (YYYY-MM-DD)                                     |
| `harvest_end`   | date    | Fecha de cosecha máxima (YYYY-MM-DD)                                     |
| `order_by`      | string  | Campo para ordenar: `name`, `price_per_unit`, `quantity`, `harvest_date` |
| `order_dir`     | string  | Dirección de orden: `asc` o `desc` (por defecto `asc`)                   |

#### Ejemplo de request

```bash
curl "http://127.0.0.1:5001/api/v1/product-search?name=ma%C3%ADz&min_price=10&order_by=price_per_unit&order_dir=desc"
```

#### Ejemplo de respuesta (200)

```json
[
  {
    "product_id": 1,
    "name": "Maíz amarillo",
    "farm_id": "FARM001",
    "type": "Grano",
    "quantity": 100,
    "price_per_unit": 25.5,
    "description": "Maíz de alta calidad",
    "harvest_date": "2025-06-01T00:00:00",
    "created_at": "2025-06-10T12:00:00"
  }
]
```

---

## 🛠️ Cómo funciona internamente

1. El **cliente** realiza el `GET /product-search` con parámetros.
2. El **Blueprint** extrae los `query params` y llama al **Caso de Uso**.
3. El **Caso de Uso** invoca al **Servicio de Dominio**.
4. El **Servicio** pide todos los productos al **adaptador HTTP**, que consume al **`ProductService`**.
5. Los datos JSON se mapean a entidades `Product`.
6. Se aplican **filtros** y **ordenamientos** en memoria.
7. El **Caso de Uso** devuelve la lista final.
8. El **Blueprint** serializa respuesta a JSON con **status 200**.

---

## 📦 Prometheus

La observabilidad permite analizar las métricas que se tienen en la API para poder comprender las dinámicas del negocio, aumentar la disponibilidad y disminuir el mantenimiento.

Se utilizó la herramienta Prometheus porque es una herramienta confiable para el análisis de las métricas. A continuación se presentan las rutas para la revisión de la información.

```bash
Targets=http://localhost:9090/targets
Query=http://localhost:9090/query
```

---

## 📜 Licencia

MIT ©
