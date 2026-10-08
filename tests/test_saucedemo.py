"""Casos de prueba automatizados sobre saucedemo.com.

Cada test usa su propio navegador (fixture `driver`), por lo que son
independientes: la falla de uno no afecta a los demás.
"""

import logging

from utils.helpers import (
    BOTON_MENU,
    FILTRO_ORDEN,
    LOGO_APP,
    TITULO_SECCION,
    agregar_primer_producto,
    esperar_visible,
    iniciar_sesion,
    ir_al_carrito,
    obtener_contador_carrito,
    obtener_nombre_y_precio,
    obtener_nombres_en_carrito,
    obtener_productos,
)

logger = logging.getLogger(__name__)


def test_login_exitoso(driver, usuario_valido):
    """Login con credenciales válidas redirige al inventario."""
    iniciar_sesion(driver, usuario_valido["username"], usuario_valido["password"])

    assert "/inventory.html" in driver.current_url, "No se redirigió a /inventory.html"
    assert esperar_visible(driver, TITULO_SECCION).text == "Products"
    assert esperar_visible(driver, LOGO_APP).text == "Swag Labs"


def test_titulo_pagina_inventario(driver_logueado):
    """El título de la pestaña en el inventario es 'Swag Labs'."""
    assert driver_logueado.title == "Swag Labs", (
        f"Título inesperado: {driver_logueado.title}"
    )


def test_productos_visibles(driver_logueado):
    """Hay al menos un producto visible; se lista nombre y precio del primero."""
    productos = obtener_productos(driver_logueado)
    assert len(productos) > 0, "No hay productos visibles en el inventario"

    nombre, precio = obtener_nombre_y_precio(productos[0])
    logger.info("Primer producto: %s - %s", nombre, precio)
    assert nombre, "El primer producto no tiene nombre"
    assert precio.startswith("$"), f"Precio con formato inesperado: {precio}"


def test_elementos_interfaz_presentes(driver_logueado):
    """El menú y el filtro de ordenamiento están visibles."""
    assert esperar_visible(driver_logueado, BOTON_MENU).is_displayed(), "Falta el menú"
    assert esperar_visible(driver_logueado, FILTRO_ORDEN).is_displayed(), "Falta el filtro"


def test_agregar_producto_al_carrito(driver_logueado):
    """Agregar el primer producto incrementa el contador y aparece en el carrito."""
    contador_inicial = obtener_contador_carrito(driver_logueado)
    nombre_producto = agregar_primer_producto(driver_logueado)

    assert obtener_contador_carrito(driver_logueado) == contador_inicial + 1, (
        "El contador del carrito no se incrementó"
    )

    ir_al_carrito(driver_logueado)
    nombres_en_carrito = obtener_nombres_en_carrito(driver_logueado)
    assert nombre_producto in nombres_en_carrito, (
        f"'{nombre_producto}' no aparece en el carrito: {nombres_en_carrito}"
    )
