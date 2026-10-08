# Pre-Entrega – Automatización QA con Selenium y Pytest

## Propósito del proyecto

Automatizar flujos básicos de navegación web sobre [saucedemo.com](https://www.saucedemo.com), un sitio demo para prácticas de testing. Las pruebas cubren:

| Test | Qué valida |
|---|---|
| `test_login_exitoso` | Login con `standard_user` / `secret_sauce`, espera explícita, redirección a `/inventory.html` y textos "Products" y "Swag Labs". |
| `test_titulo_pagina_inventario` | El título de la página de inventario es "Swag Labs". |
| `test_productos_visibles` | Hay al menos un producto visible. Registra el nombre y el precio del primero. |
| `test_elementos_interfaz_presentes` | El menú y el filtro de ordenamiento están visibles. |
| `test_agregar_producto_al_carrito` | Agrega el primer producto, verifica que el contador del carrito sube a 1, entra al carrito y comprueba que el producto está ahí. |

Cada test abre su propio navegador, así que son independientes: si uno falla, los demás no se ven afectados.

## Tecnologías utilizadas

- **Python 3** – lenguaje principal
- **Pytest** – estructura y ejecución de las pruebas
- **Selenium WebDriver** – automatización del navegador (Google Chrome)
- **pytest-html** – reporte HTML de resultados
- **Git y GitHub** – control de versiones

## Estructura del proyecto

```
pre-entrega-automation-testing-maryfranks-tovar/
├── tests/
│   ├── conftest.py          # Fixtures (navegador, login) y captura automática ante fallos
│   └── test_saucedemo.py    # Casos de prueba
├── utils/
│   ├── config.py            # URL, tiempos de espera, rutas y lectura de datos
│   └── helpers.py           # Localizadores y funciones auxiliares (login, carrito, etc.)
├── datos/
│   └── usuarios.json        # Credenciales de prueba
├── reports/
│   ├── reporte.html         # Reporte HTML generado por Pytest
│   ├── ejecucion.log        # Log de la ejecución
│   └── screenshots/         # Capturas automáticas cuando falla un test
├── pytest.ini               # Configuración de Pytest y logs
├── requirements.txt         # Dependencias
└── README.md
```

## Instalación de dependencias

Requisitos previos: Python 3.10 o superior y Google Chrome instalados. Selenium Manager descarga el ChromeDriver adecuado automáticamente.

```bash
git clone https://github.com/Maryfranks23/pre-entrega-automation-testing-maryfranks-tovar.git
cd pre-entrega-automation-testing-maryfranks-tovar
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución de las pruebas

Ejecutar todos los tests y generar el reporte HTML:

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Por defecto el navegador corre en modo *headless* (sin ventana). Para ver el navegador mientras se ejecutan las pruebas:

```bash
# Windows (PowerShell)
$env:HEADLESS="0"; pytest -v --html=reports/reporte.html --self-contained-html
# Linux / macOS
HEADLESS=0 pytest -v --html=reports/reporte.html --self-contained-html
```

## Evidencias

- **Reporte HTML:** `reports/reporte.html`, con el resultado de cada test.
- **Logs:** `reports/ejecucion.log`, con cada paso ejecutado (login, producto agregado, etc.).
- **Capturas ante fallos:** si un test falla, se guarda automáticamente una captura en `reports/screenshots/` y además se adjunta dentro del reporte HTML.
