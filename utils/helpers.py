"""Funciones auxiliares reutilizables para interactuar con saucedemo.com."""

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import TIEMPO_ESPERA, URL_BASE

logger = logging.getLogger(__name__)

# --- Localizadores (centralizados para facilitar el mantenimiento) ---
CAMPO_USUARIO = (By.ID, "user-name")
CAMPO_PASSWORD = (By.ID, "password")
BOTON_LOGIN = (By.ID, "login-button")
TITULO_SECCION = (By.CLASS_NAME, "title")
LOGO_APP = (By.CLASS_NAME, "app_logo")
BOTON_MENU = (By.ID, "react-burger-menu-btn")
FILTRO_ORDEN = (By.CLASS_NAME, "product_sort_container")
ITEMS_INVENTARIO = (By.CLASS_NAME, "inventory_item")
NOMBRE_ITEM = (By.CLASS_NAME, "inventory_item_name")
PRECIO_ITEM = (By.CLASS_NAME, "inventory_item_price")
BOTON_AGREGAR = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
CONTADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")
ICONO_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
ITEMS_CARRITO = (By.CLASS_NAME, "cart_item")


def crear_driver(headless=True):
    """Crea y devuelve una instancia de Chrome WebDriver."""
    opciones = webdriver.ChromeOptions()
    if headless:
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1920,1080")
    opciones.add_argument("--incognito")
    # Evita el popup de "contraseña filtrada" de Chrome, que tapa la página
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    logger.info("Iniciando Chrome (headless=%s)", headless)
    return webdriver.Chrome(options=opciones)


def esperar_visible(driver, localizador):
    """Espera explícitamente a que un elemento sea visible y lo devuelve."""
    return WebDriverWait(driver, TIEMPO_ESPERA).until(
        EC.visibility_of_element_located(localizador)
    )


def esperar_todos_visibles(driver, localizador):
    """Espera a que los elementos sean visibles y devuelve la lista."""
    return WebDriverWait(driver, TIEMPO_ESPERA).until(
        EC.visibility_of_all_elements_located(localizador)
    )


def iniciar_sesion(driver, usuario, password):
    """Navega a la página de login, ingresa credenciales y espera el inventario."""
    logger.info("Navegando a %s", URL_BASE)
    driver.get(URL_BASE)
    esperar_visible(driver, CAMPO_USUARIO).send_keys(usuario)
    driver.find_element(*CAMPO_PASSWORD).send_keys(password)
    driver.find_element(*BOTON_LOGIN).click()
    # Espera explícita hasta que la URL cambie a la página de inventario
    WebDriverWait(driver, TIEMPO_ESPERA).until(EC.url_contains("/inventory.html"))
    logger.info("Login realizado con el usuario '%s'", usuario)


def obtener_productos(driver):
    """Devuelve la lista de productos visibles en el inventario."""
    return esperar_todos_visibles(driver, ITEMS_INVENTARIO)


def obtener_nombre_y_precio(producto):
    """Devuelve (nombre, precio) de un elemento de producto."""
    nombre = producto.find_element(*NOMBRE_ITEM).text
    precio = producto.find_element(*PRECIO_ITEM).text
    return nombre, precio


def agregar_primer_producto(driver):
    """Agrega el primer producto del inventario al carrito y devuelve su nombre."""
    primer_producto = obtener_productos(driver)[0]
    nombre, _ = obtener_nombre_y_precio(primer_producto)
    primer_producto.find_element(*BOTON_AGREGAR).click()
    logger.info("Producto agregado al carrito: %s", nombre)
    return nombre


def obtener_contador_carrito(driver):
    """Devuelve el número que muestra el ícono del carrito (0 si no hay badge)."""
    badges = driver.find_elements(*CONTADOR_CARRITO)
    return int(badges[0].text) if badges else 0


def ir_al_carrito(driver):
    """Hace clic en el ícono del carrito y espera la página del carrito."""
    driver.find_element(*ICONO_CARRITO).click()
    WebDriverWait(driver, TIEMPO_ESPERA).until(EC.url_contains("/cart.html"))
    logger.info("Navegó al carrito")


def obtener_nombres_en_carrito(driver):
    """Devuelve los nombres de los productos presentes en el carrito."""
    items = esperar_todos_visibles(driver, ITEMS_CARRITO)
    return [item.find_element(*NOMBRE_ITEM).text for item in items]
