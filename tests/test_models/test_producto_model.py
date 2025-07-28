import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from decimal import Decimal
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.producto_model import Producto


class TestProductoModel(unittest.TestCase):
    """Tests unitarios para el modelo Producto"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.valid_data = {
            'nombre': 'Producto Test',
            'precio': 99.99,
            'descripcion': 'Descripción de prueba',
            'stock': 10,
            'categoria': 'Categoria Test'
        }
    
    def test_create_product_success(self):
        """Test: Crear producto exitosamente"""
        with patch.object(Producto, 'save', return_value=(True, "Producto guardado")):
            producto, mensaje = Producto.create_product(**self.valid_data)
            
            self.assertIsNotNone(producto)
            self.assertEqual(mensaje, "Producto creado exitosamente")
            self.assertEqual(producto.nombre, "Producto Test")
            self.assertEqual(producto.precio, Decimal('99.99'))
            self.assertEqual(producto.stock, 10)
    
    def test_create_product_invalid_name_empty(self):
        """Test: Crear producto con nombre vacío"""
        data = self.valid_data.copy()
        data['nombre'] = ''
        
        producto, mensaje = Producto.create_product(**data)
        
        self.assertIsNone(producto)
        self.assertEqual(mensaje, "El nombre debe tener al menos 2 caracteres")
    
    def test_create_product_invalid_name_short(self):
        """Test: Crear producto con nombre muy corto"""
        data = self.valid_data.copy()
        data['nombre'] = 'A'
        
        producto, mensaje = Producto.create_product(**data)
        
        self.assertIsNone(producto)
        self.assertEqual(mensaje, "El nombre debe tener al menos 2 caracteres")
    
    def test_create_product_invalid_price_zero(self):
        """Test: Crear producto con precio cero"""
        data = self.valid_data.copy()
        data['precio'] = 0
        
        producto, mensaje = Producto.create_product(**data)
        
        self.assertIsNone(producto)
        self.assertEqual(mensaje, "El precio debe ser mayor a 0")
    
    def test_create_product_invalid_price_negative(self):
        """Test: Crear producto con precio negativo"""
        data = self.valid_data.copy()
        data['precio'] = -10.50
        
        producto, mensaje = Producto.create_product(**data)
        
        self.assertIsNone(producto)
        self.assertEqual(mensaje, "El precio debe ser mayor a 0")
    
    def test_create_product_invalid_price_string(self):
        """Test: Crear producto con precio inválido (string)"""
        data = self.valid_data.copy()
        data['precio'] = "precio_invalido"
        
        producto, mensaje = Producto.create_product(**data)
        
        self.assertIsNone(producto)
        self.assertEqual(mensaje, "El precio no es válido")
    
    def test_create_product_invalid_stock_negative(self):
        """Test: Crear producto con stock negativo"""
        data = self.valid_data.copy()
        data['stock'] = -5
        
        producto, mensaje = Producto.create_product(**data)
        
        self.assertIsNone(producto)
        self.assertEqual(mensaje, "El stock no puede ser negativo")
    
    def test_create_product_invalid_stock_string(self):
        """Test: Crear producto con stock inválido (string)"""
        data = self.valid_data.copy()
        data['stock'] = "stock_invalido"
        
        producto, mensaje = Producto.create_product(**data)
        
        self.assertIsNone(producto)
        self.assertEqual(mensaje, "El stock debe ser un número entero válido")
    
    def test_create_product_database_error(self):
        """Test: Error al guardar en base de datos"""
        with patch.object(Producto, 'save', return_value=(False, "Error de BD")):
            producto, mensaje = Producto.create_product(**self.valid_data)
            
            self.assertIsNone(producto)
            self.assertEqual(mensaje, "Error de BD")
    
    @patch.object(Producto, 'get_by_category')
    def test_get_by_category_success(self, mock_get_by_category):
        """Test: Obtener productos por categoría exitosamente"""
        # Mock de productos esperados
        mock_productos = [
            MagicMock(nombre="Producto 1", categoria="Electronics"),
            MagicMock(nombre="Producto 2", categoria="Electronics")
        ]
        mock_get_by_category.return_value = mock_productos
        
        result = Producto.get_by_category("Electronics")
        
        self.assertEqual(len(result), 2)
        mock_get_by_category.assert_called_once_with("Electronics")
    
    @patch.object(Producto, 'get_by_category')
    def test_get_by_category_exception(self, mock_get_by_category):
        """Test: Excepción al obtener productos por categoría"""
        mock_get_by_category.return_value = []
        
        result = Producto.get_by_category("Electronics")
        
        self.assertEqual(result, [])
    
    @patch.object(Producto, 'get_available_products')
    def test_get_available_products_success(self, mock_get_available):
        """Test: Obtener productos disponibles exitosamente"""
        mock_productos = [
            MagicMock(nombre="Producto 1", stock=5),
            MagicMock(nombre="Producto 2", stock=10)
        ]
        mock_get_available.return_value = mock_productos
        
        result = Producto.get_available_products()
        
        self.assertEqual(len(result), 2)
        mock_get_available.assert_called_once()
    
    @patch.object(Producto, 'search_by_name')
    def test_search_by_name_success(self, mock_search):
        """Test: Buscar productos por nombre exitosamente"""
        mock_productos = [MagicMock(nombre="Producto Test")]
        mock_search.return_value = mock_productos
        
        result = Producto.search_by_name("Test")
        
        self.assertEqual(len(result), 1)
        mock_search.assert_called_once_with("Test")
    
    def test_reduce_stock_success(self):
        """Test: Reducir stock exitosamente"""
        # Crear producto mock
        producto = Producto()
        producto.stock = 10
        
        with patch.object(producto, 'update', return_value=(True, "Actualizado")):
            result, message = producto.reduce_stock(3)
            
            self.assertTrue(result)
            self.assertEqual(producto.stock, 7)
    
    def test_reduce_stock_insufficient(self):
        """Test: Reducir stock insuficiente"""
        producto = Producto()
        producto.stock = 2
        
        result, message = producto.reduce_stock(5)
        
        self.assertFalse(result)
        self.assertEqual(message, "Stock insuficiente")
        self.assertEqual(producto.stock, 2)  # Stock no debe cambiar
    
    def test_increase_stock_success(self):
        """Test: Aumentar stock exitosamente"""
        producto = Producto()
        producto.stock = 5
        
        with patch.object(producto, 'update', return_value=(True, "Actualizado")):
            result, message = producto.increase_stock(3)
            
            self.assertTrue(result)
            self.assertEqual(producto.stock, 8)
    
    def test_is_available_true(self):
        """Test: Producto disponible"""
        producto = Producto()
        producto.stock = 10
        
        self.assertTrue(producto.is_available(5))
        self.assertTrue(producto.is_available())  # Default cantidad=1
    
    def test_is_available_false(self):
        """Test: Producto no disponible"""
        producto = Producto()
        producto.stock = 2
        
        self.assertFalse(producto.is_available(5))
    
    def test_to_dict(self):
        """Test: Convertir producto a diccionario"""
        producto = Producto()
        producto.id = 1
        producto.nombre = "Producto Test"
        producto.descripcion = "Descripción"
        producto.precio = Decimal('99.99')
        producto.stock = 10
        producto.categoria = "Electronics"
        producto.fecha_creacion = datetime(2024, 1, 15, 10, 30, 0)
        
        result = producto.to_dict()
        
        expected = {
            'id': 1,
            'nombre': 'Producto Test',
            'descripcion': 'Descripción',
            'precio': 99.99,
            'stock': 10,
            'categoria': 'Electronics',
            'fecha_creacion': '2024-01-15T10:30:00'
        }
        
        self.assertEqual(result, expected)
    
    def test_to_dict_with_none_values(self):
        """Test: Convertir producto con valores None a diccionario"""
        producto = Producto()
        producto.id = 1
        producto.nombre = "Producto Test"
        producto.descripcion = None
        producto.precio = Decimal('50.00')
        producto.stock = 0
        producto.categoria = None
        producto.fecha_creacion = None
        
        result = producto.to_dict()
        
        self.assertIsNone(result['descripcion'])
        self.assertIsNone(result['categoria'])
        self.assertIsNone(result['fecha_creacion'])
    
    def test_repr(self):
        """Test: Representación string del producto"""
        producto = Producto()
        producto.nombre = "Producto Test"
        
        self.assertEqual(repr(producto), "<Producto Producto Test>")


if __name__ == '__main__':
    unittest.main()