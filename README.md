# Wi-Point API

API para consultar los puntos de acceso WiFi publicos de la Ciudad de Mexico. Construida con FastAPI, GraphQL (Strawberry) y PostgreSQL + PostGIS para queries geoespaciales.

## Como lo hice

Desarrolle una API GraphQL que consume datos abiertos de la CDMX sobre puntos WiFi publicos. El proyecto incluye un scraper que obtiene automaticamente el archivo Excel desde el portal de datos abiertos, lo procesa y lo carga a una base de datos PostgreSQL con extension PostGIS para poder hacer consultas por proximidad geografica.

### Flujo de trabajo

1. Analice el archivo Excel para definir el modelado de datos
2. Investigue que stack serviria para manejar coordenadas geograficas (PostGIS + GeoAlchemy2)
3. Diseñe la estructura de carpetas del proyecto
4. Planifique como hacer la carga de datos del Excel a la base de datos
5. Hice un borrador con archivos y carpetas para visualizar la comunicacion entre componentes
6. Cree un diagrama de flujo en draw.io
7. Con todo definido (modelo, carga, stack, estructura, diagrama) empece a codear

## Stack

| Tecnologia | Uso |
|---|---|
| **FastAPI** | Framework web |
| **Strawberry GraphQL** | API GraphQL con tipado |
| **PostgreSQL 16 + PostGIS 3.4** | Base de datos con soporte geoespacial |
| **SQLAlchemy 2.0** | ORM |
| **Alembic** | Migraciones de base de datos |
| **GeoAlchemy2** | Columnas y queries geoespaciales |
| **Pandas** | Procesamiento del Excel |
| **BeautifulSoup4** | Scraping del portal de datos abiertos |
| **Docker Compose** | Orquestacion de servicios |

### Testing

| Tecnologia | Uso |
|---|---|
| **pytest** | Framework de tests |
| **TestClient (FastAPI)** | Cliente HTTP para tests sin levantar servidor |
| **factory-boy** | Generacion de datos fake |
| **graphql-query** | Construccion de queries GraphQL con clases Python |
| **pytest-cov** | Cobertura de codigo |

## Carga de datos

La carga de datos se ejecuta automaticamente al iniciar la API y combina tres mecanismos clave:

### Scraper

La clase `ScraperWiFiPoints` hace scraping al portal [datos.cdmx.gob.mx](https://datos.cdmx.gob.mx/dataset/puntos-de-acceso-wifi-en-la-cdmx) para:

- Extraer la fecha de ultima actualizacion del dataset
- Obtener la URL de descarga del archivo Excel
- Descargar el archivo como bytes

Si la fecha del portal es mas reciente que la ultima carga registrada en la base de datos, se procede con la actualizacion. Si no, se omite.

### Paralelismo

La clase `WifiPointLoader` divide el DataFrame en batches de 1000 registros y los inserta en paralelo usando `ThreadPoolExecutor` con 5 workers. Cada worker maneja su propia sesion de base de datos para evitar conflictos.

### Upsert

Cada batch usa `INSERT ... ON CONFLICT DO UPDATE` (upsert) sobre el campo `original_id`. Si el registro ya existe, se actualizan sus campos (`program`, `town_hall`, `lat`, `ltg`). Esto permite re-ejecutar la carga sin duplicar datos ni perder actualizaciones.

```python
stmt = insert(WifiPoint).values(data)
stmt = stmt.on_conflict_do_update(
    index_elements=[WifiPoint.original_id],
    set_={
        "program": stmt.excluded.program,
        "town_hall": stmt.excluded.town_hall,
        "lat": stmt.excluded.lat,
        "ltg": stmt.excluded.ltg,
    }
)
```

### Diagrama de Flujo

![Diagrama de flujo](Flujo%20carga%20de%20datos.png)

Despues de insertar todos los batches, se actualizan las columnas PostGIS `location` para los registros que aun no la tienen:

```sql
UPDATE wifi_points
SET location = ST_SetSRID(ST_MakePoint(ltg, lat), 4326)::geography
WHERE location IS NULL AND lat != 0 AND ltg != 0
```

## Migraciones con Alembic

El proyecto usa Alembic para versionar los cambios en la base de datos. Cada cambio en los modelos SQLAlchemy se refleja en un archivo de migracion.

```bash
# Crear una nueva migracion a partir de cambios en los modelos
make migration m="descripcion del cambio"

# Aplicar migraciones pendientes
make migrate

# Revertir la ultima migracion
make downgrade
```

Las migraciones se aplican automaticamente al levantar el contenedor (`alembic upgrade head` en el CMD del Dockerfile).

## Estructura del proyecto

```
wi-point-api/
├── docker-compose.yml
├── Makefile
├── .env
│
└── backend/
    ├── Dockerfile
    ├── pytest.ini
    ├── alembic.ini
    ├── alembic/
    │   └── versions/              # Archivos de migracion
    │
    ├── app/
    │   ├── main.py                # Entry point FastAPI + GraphQL router
    │   ├── requirements.txt
    │   │
    │   ├── core/
    │   │   ├── base.py            # Modelo base SQLAlchemy (id, timestamps)
    │   │   ├── config.py          # Settings con Pydantic
    │   │   └── database.py        # Engine y SessionLocal
    │   │
    │   ├── seed/
    │   │   ├── main.py            # Orquestador del seed
    │   │   ├── scraper.py         # Scraping del portal de datos abiertos
    │   │   └── loader.py          # Carga con batches, hilos y upsert
    │   │
    │   └── src/
    │       ├── graphql/
    │       │   ├── schema.py      # Schema y router GraphQL
    │       │   ├── extensions.py  # Inyeccion de sesion DB al contexto
    │       │   └── resolvers/
    │       │       └── wifi_point_query.py
    │       │
    │       ├── models/
    │       │   ├── wifi_point.py
    │       │   └── wifi_point_version.py
    │       │
    │       ├── schemas/
    │       │   ├── wifi_point_graphql.py
    │       │   ├── pagination_params_graphql.py
    │       │   └── paginated_response_graphql.py
    │       │
    │       ├── providers/
    │       │   ├── wifi_point.py
    │       │   └── wifi_point_version.py
    │       │
    │       └── helpers/
    │           └── filters.py     # Filtros y orden por proximidad
    │
    └── tests/
        ├── conftest.py            # Fixtures globales (client, mock_db)
        ├── test_health.py
        │
        ├── factories/
        │   └── wifi_point.py      # Factory con factory-boy
        │
        ├── graphql/
        │   ├── test_wifi_points.py
        │   └── queries/
        │       ├── wifi_point_query.py
        │       └── wifi_points_query.py
        │
        └── providers/
            └── test_wifi_point.py
```

## Levantar el proyecto

### Requisitos

- Docker y Docker Compose

### Comandos

Todos los comandos estan en el `Makefile`:

```bash
# Levantar todo (PostgreSQL + API)
make up

# Ver logs de la API
make logs

# Apagar todo
make down

# Reiniciar solo la API
make restart-api

# Ejecutar tests
make tests

# Ejecutar tests con reporte de cobertura
make coverage
```

Al hacer `make up`, la API queda disponible en:

**http://localhost:8000/graphql**

