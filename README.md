# FoodCraft

FoodCraft es una aplicacion de recetas con una interfaz de terminal (CLI) hecha con Rich.

La UI permite:
- Ver listados de entidades (Users, Recipes, Categories, Ingredients, Ratings).
- Entrar en submenus de acciones para Users y Recipes.
- Ejecutar operaciones CRUD basicas contra la base de datos.

## UI de FoodCraft

### Como se organiza

- Menu principal: `src/foodcraft/app_ui.py`
- Menús y acciones de usuarios y recetas: `src/foodcraft/app_ui.py`
- Comunicación con la API: `src/foodcraft/api_client.py`

Flujo general:
1. Se muestra el logo y el menu principal.
2. Si eliges Users o Recipes, primero ves el listado actual.
3. Despues se abre el submenu de acciones (Add, Update, Delete, Get, GetAll).

### Como ejecutar la UI

Desde la raiz del proyecto (Windows PowerShell):

```powershell
$env:PYTHONPATH = "src"
python -m foodcraft.app_ui
```

Si usas otro terminal:

```bash
PYTHONPATH=src python -m foodcraft.app_ui
```

## API (en construccion)

La base de la API HTTP/REST (URLs, Requests, Responses) esta documentada en [src/api/README.md](src/api/README.md).

## Seguridad: TLS 1.3

Los dos tramos (UI -> API y API -> backend) usan TLS 1.3. Cada cliente comprueba el certificado del
servidor mediante una CA local. TLS cifra la conexion y valida el servidor, pero no identifica al
cliente: no se piden certificados de cliente (sin mTLS). La configuracion esta en
[src/security/tls.py](src/security/tls.py). No hace falta una carpeta `network`: cada servidor
mantiene su socket donde ya esta implementado.

Genera una CA local y un certificado por servidor:

```powershell
pip install cryptography            # solo hace falta al generar los certificados
python scripts/generate_certificates.py
```

Los archivos se guardan en `certs/` y no se deben subir a Git. La UI usa
`https://127.0.0.1:8000` por defecto (`API_URL` para cambiarlo); los certificados generados son
validos para `localhost` y `127.0.0.1`. Si se despliega en otros equipos, hay que generar
certificados que incluyan sus nombres o IPs. Python utiliza PEM directamente, asi que no hace falta
un archivo `.p12`.

Diagrama draw.io detallado (certificados, handshakes TLS y ejemplo de peticion/respuesta): [src/api/flujo-tls.drawio](src/api/flujo-tls.drawio).

## Menus disponibles

### Main menu

- 1: Users
- 2: Recipes
- 3: Categories
- 4: Ingredients
- 5: Ratings
- 0: Exit

### Users menu

- 1: Add
- 2: Update
- 3: Delete
- 4: Get
- 5: GetAll
- 0: Exit

### Recipes menu

- 1: Add
- 2: Update
- 3: Delete
- 4: Get
- 5: GetAll
- 0: Exit

## Notas practicas

- Para crear o actualizar una receta, el Author user ID debe existir.
- Los cambios se guardan en base de datos al confirmar cada accion.
- Si una entidad no existe, la UI muestra un mensaje claro y vuelve al flujo normal.

## Migrations (Alembic)

Generar una migracion:

```bash
alembic revision --autogenerate -m "describe your change"
```

Aplicar migraciones:

```bash
alembic upgrade head
```