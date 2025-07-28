# Archivo principal de modelos - Importa todos los modelos
from models.usuario_model import Usuario
from models.producto_model import Producto  
from models.pedido_model import Pedido

# Exportar para facilitar importación
__all__ = ['Usuario', 'Producto', 'Pedido']