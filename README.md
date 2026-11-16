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

## Seguridad: TLS 1.3 con autenticacion mutua

Los dos tramos (UI -> API y API -> backend) van cifrados con TLS 1.3 usando solo el modulo `ssl`
([src/security/tls.py](src/security/tls.py)). Cada extremo presenta su certificado (mTLS): el
cifrado asimetrico negocia la clave de sesion y los datos se cifran con cifrado simetrico (AEAD).

Antes del primer arranque, genera la CA y los certificados (las claves `*.key` no se versionan):

```powershell
pip install cryptography            # solo para generar los certificados
python scripts/generate_certificates.py
```

Si quieres las claves cifradas, define `TLS_KEY_PASSWORD` antes de generarlas y tambien al arrancar
cada servicio. La UI usa `https://127.0.0.1:8000` por defecto (`API_URL` para cambiarlo); los
certificados son validos para `localhost` y `127.0.0.1`.

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