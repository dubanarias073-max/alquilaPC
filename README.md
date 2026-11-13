# ALQUILAPC – Liquidación de alquiler de portátiles

Aplicación web en **Django** que liquida, factura y consulta servicios de alquiler de portátiles por días ($35.000 por equipo/día). **No usa base de datos** para los servicios: se guardan en memoria mientras el servidor esté encendido.

Autor: DUBAN Alejandro Arias B · Ficha 3407184 · ADSO – SENA

## Requisitos
- Python 3.10 o superior (`python --version`)

## Instalación y ejecución desde cero

> **Importante:** todos los comandos se ejecutan en la carpeta donde está `manage.py` (junto a `requirements.txt`, `liquidacion/` y `tests/`). Al descomprimir el zip se crea `AlquilaPC\AlquilaPC\`; no entres a la subcarpeta `alquilapc` (la configuración de Django), porque en Windows `AlquilaPC` y `alquilapc` se ven como el mismo nombre. Para comprobar que estás en el lugar correcto: `dir manage.py` (Windows) o `ls manage.py` (Linux/macOS).

### Windows (PowerShell / CMD)
```bat
cd AlquilaPC
dir manage.py
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Linux / macOS
```bash
cd AlquilaPC
ls manage.py
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Abrir **http://127.0.0.1:8000/**

### Versión de consola (sin servidor)
```bash
python proyecto1.py
```
Pide los datos por teclado y muestra el recibo en la terminal. Usa las mismas reglas de negocio que la app web.

### Solución de problemas
| Error | Causa | Solución |
|---|---|---|
| `can't open file '...\manage.py'` | Estás dentro de la subcarpeta `alquilapc` | `cd ..` y verificar con `dir manage.py` |
| El `venv` quedó dentro de `alquilapc` | Se creó en la carpeta equivocada | `deactivate`, `Remove-Item -Recurse -Force .\venv`, `cd ..` y crearlo de nuevo |
| `activate` bloqueado en PowerShell | Política de ejecución | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `No module named django` | No se activó el `venv` o no se instalaron dependencias | `venv\Scripts\activate` y `pip install -r requirements.txt` |

> Sobre las migraciones: la app `liquidacion` no tiene modelos (requisito: sin base de datos), así que `makemigrations` responde *No changes detected*. `migrate` solo crea las tablas internas de Django en `db.sqlite3`. Las liquidaciones no se guardan ahí.

## Uso
| Ruta | Función |
|---|---|
| `/` | Formulario para liquidar + consulta + lista de servicios |
| `POST /liquidar/` | Valida, calcula y genera la factura |
| `/servicio/<n>/` | Recibo del servicio N.º n (botón **Imprimir recibo**) |
| `/consultar/?numero=n` | Consulta un servicio por número |


## Reglas de negocio
1. Valor alquiler = equipos × días iniciales × $35.000 (mínimo 2 equipos).
2. Días adicionales: valor = equipos × días adicionales × $35.000, con **2 % de descuento** sobre ese valor.
3. En el establecimiento: **5 % de descuento** sobre el total (después del 2 %).
4. Fuera de la ciudad: **5 % de cargo** sobre el total (después de descuentos).

Ejemplo (5 eq, 4 días, 3 adic): ciudad **$1.214.500** · fuera **$1.275.225** · establecimiento **$1.153.775**.

## Pruebas automatizadas (unittest, equivalente a JUnit)
```bash
python manage.py test tests -v 2
```
| Archivo | Tipo | Casos |
|---|---|---:|
| `tests/test_caja_negra.py` | Caja negra: partición de equivalencia, valores límite, S01–S05 | 28 |
| `tests/test_caja_blanca.py` | Caja blanca: cada función y rama if/else | 19 |
| `tests/test_regresion.py` | Regresión: valores aprobados | 4 |
| `tests/test_web.py` | Integración/sistema: vistas, recibo, consulta | 13 |

Solo la lógica, sin Django: `python -m unittest tests.test_caja_negra tests.test_caja_blanca tests.test_regresion -v`

## Pruebas en el navegador (caja negra, CP001–CP028)
```bash
pip install playwright
python -m playwright install chromium
python manage.py runserver --noreload        # terminal 1 (servidor recién iniciado)
python pruebas_ui/ejecutar_casos_ui.py --ronda 1   # terminal 2
```
Guarda una captura por caso y `resultados.json` en `docs/evidencias/ronda1/`.

## Pruebas manuales
- **Caja negra:** abrir la página y seguir la hoja *Casos caja negra* de `docs/matriz-casos-de-prueba-iso29119.xlsx` (entradas → resultado esperado). Anotar lo obtenido y el estado.
- **Caja blanca:** abrir `liquidacion/calculos.py`, recorrer cada `if/else` con los datos de la hoja *Casos caja blanca* y comprobar el valor de cada función (`python manage.py shell` → `from liquidacion.calculos import *`).
- **Regresión:** después de cualquier cambio, volver a ejecutar todos los casos aprobados (hoja *Regresión*) y `python manage.py test tests`.

## Estructura
```
AlquilaPC/
├── alquilapc/              configuración Django
├── liquidacion/
│   ├── calculos.py         reglas de negocio (funciones del diagrama)
│   ├── repositorio.py      almacenamiento en memoria
│   ├── views.py  urls.py   vistas: inicio, liquidar, recibo, consultar
│   └── templates/ static/
├── proyecto1.py            versión consola
├── tests/                  unittest
├── pruebas_ui/             casos CP001–CP028 + ejecutor en navegador
└── docs/
    ├── Descripcion_funcional.md   Product_Backlog.md   Plan_de_Pruebas.md
    ├── Prompts.md                 Informe_de_hallazgos.md
    ├── matriz-casos-de-prueba-iso29119.xlsx
    ├── uml/                casos de uso, clases, secuencia, actividad (.mmd + .png)
    └── evidencias/         capturas ronda 1 y 2, salida de unittest
```