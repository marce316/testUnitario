import pytest
import sys
import os
from unittest.mock import MagicMock

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_db():
    """Mock de la base de datos para testing"""
    db_mock = MagicMock()
    return db_mock

@pytest.fixture
def sample_producto_data():
    """Datos de ejemplo para tests de productos"""
    return {
        'nombre': 'Producto Test',
        'precio': 99.99,
        'descripcion': 'Descripción de prueba',
        'stock': 10,
        'categoria': 'Categoria Test'
    }

@pytest.fixture
def invalid_producto_data():
    """Datos inválidos para tests de productos"""
    return {
        'nombre': '',  # Nombre vacío
        'precio': -10,  # Precio negativo
        'stock': -5,   # Stock negativo
        'categoria': None
    }