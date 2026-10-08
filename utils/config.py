"""Configuración general del proyecto: URLs, tiempos de espera y rutas."""

import json
from pathlib import Path

# URL base del sitio bajo prueba
URL_BASE = "https://www.saucedemo.com/"

# Tiempo máximo (segundos) de las esperas explícitas
TIEMPO_ESPERA = 10

# Rutas del proyecto
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS = RAIZ_PROYECTO / "datos"
CARPETA_CAPTURAS = RAIZ_PROYECTO / "reports" / "screenshots"


def cargar_usuario(clave="usuario_valido"):
    """Lee las credenciales de prueba desde datos/usuarios.json."""
    with open(CARPETA_DATOS / "usuarios.json", encoding="utf-8") as archivo:
        return json.load(archivo)[clave]
