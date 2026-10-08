"""Fixtures compartidas y captura automática de pantalla ante fallos."""

import logging
import os
from datetime import datetime

import pytest

from utils.config import CARPETA_CAPTURAS, cargar_usuario
from utils.helpers import crear_driver, iniciar_sesion

logger = logging.getLogger(__name__)


@pytest.fixture
def driver():
    """Abre un navegador nuevo por test y lo cierra al final (tests independientes)."""
    headless = os.getenv("HEADLESS", "1") != "0"
    navegador = crear_driver(headless=headless)
    yield navegador
    navegador.quit()
    logger.info("Navegador cerrado")


@pytest.fixture
def usuario_valido():
    """Credenciales válidas leídas desde datos/usuarios.json."""
    return cargar_usuario("usuario_valido")


@pytest.fixture
def driver_logueado(driver, usuario_valido):
    """Navegador con la sesión ya iniciada en saucedemo.com."""
    iniciar_sesion(driver, usuario_valido["username"], usuario_valido["password"])
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda una captura y la adjunta al reporte HTML."""
    resultado = yield
    reporte = resultado.get_result()
    if reporte.when != "call" or not reporte.failed:
        return

    navegador = item.funcargs.get("driver")
    if navegador is None:
        return

    CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = CARPETA_CAPTURAS / f"{item.name}_{marca}.png"
    navegador.save_screenshot(str(ruta))
    logger.error("Test fallido. Captura guardada en %s", ruta)

    # Adjunta la captura dentro del reporte de pytest-html
    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is not None:
        extras = getattr(reporte, "extras", [])
        extras.append(pytest_html.extras.png(navegador.get_screenshot_as_base64()))
        reporte.extras = extras
