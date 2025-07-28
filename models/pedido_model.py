from models import db
from models.base_model import BaseModel
from datetime import datetime
from sqlalchemy import Numeric
from decimal import Decimal

class Pedido(BaseModel, db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_total = db.Column(Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pedido {self.id}>'
    
    # Métodos específicos del modelo Pedido
    @classmethod
    def create_order(cls, usuario_id, producto_id, cantidad):
        """Crear un nuevo pedido con validación"""
        try:
            # Importar aquí para evitar circular imports
            from models.usuario_model import Usuario
            from models.producto_model import Producto
            
            # Validaciones básicas
            if not usuario_id or not producto_id or not cantidad:
                return None, "Todos los campos son requeridos"
            
            if cantidad <= 0:
                return None, "La cantidad debe ser mayor a 0"
            
            # Verificar que existe el usuario
            usuario = Usuario.get_by_id(usuario_id)
            if not usuario:
                return None, "El usuario no existe"
            
            # Verificar que existe el producto
            producto = Producto.get_by_id(producto_id)
            if not producto:
                return None, "El producto no existe"
            
            # Verificar stock disponible
            if not producto.is_available(cantidad):
                return None, f"Stock insuficiente. Disponible: {producto.stock}"
            
            # Calcular precio total
            precio_total = Decimal(str(producto.precio)) * cantidad
            
            # Crear pedido
            pedido = cls(
                usuario_id=usuario_id,
                producto_id=producto_id,
                cantidad=cantidad,
                precio_total=precio_total,
                estado='pendiente'
            )
            
            # Guardar pedido
            success, message = pedido.save()
            if success:
                # Reducir stock del producto
                stock_success, stock_message = producto.reduce_stock(cantidad)
                if not stock_success:
                    # Si falla la reducción de stock, eliminar el pedido
                    pedido.delete()
                    return None, f"Error al actualizar stock: {stock_message}"
                
                return pedido, "Pedido creado exitosamente"
            else:
                return None, message
                
        except Exception as e:
            return None, f"Error inesperado: {str(e)}"
    
    @classmethod
    def get_orders_with_details(cls):
        """Obtener pedidos con información de usuario y producto"""
        try:
            from models.usuario_model import Usuario
            from models.producto_model import Producto
            
            return db.session.query(cls, Usuario, Producto).join(
                Usuario, cls.usuario_id == Usuario.id
            ).join(
                Producto, cls.producto_id == Producto.id
            ).all()
        except Exception as e:
            print(f"Error al obtener pedidos con detalles: {e}")
            return []
    
    @classmethod
    def get_by_user(cls, usuario_id):
        """Obtener pedidos de un usuario específico"""
        try:
            return cls.query.filter_by(usuario_id=usuario_id).all()
        except Exception as e:
            print(f"Error al obtener pedidos por usuario: {e}")
            return []
    
    @classmethod
    def get_by_status(cls, estado):
        """Obtener pedidos por estado"""
        try:
            return cls.query.filter_by(estado=estado).all()
        except Exception as e:
            print(f"Error al obtener pedidos por estado: {e}")
            return []
    
    def update_status(self, nuevo_estado):
        """Actualizar estado del pedido"""
        estados_validos = ['pendiente', 'procesando', 'enviado', 'entregado', 'cancelado']
        if nuevo_estado not in estados_validos:
            return False, f"Estado inválido. Estados válidos: {estados_validos}"
        
        return self.update(estado=nuevo_estado)
    
    def cancel_order(self):
        """Cancelar pedido y restaurar stock"""
        try:
            from models.producto_model import Producto
            
            if self.estado == 'cancelado':
                return False, "El pedido ya está cancelado"
            
            # Restaurar stock
            producto = Producto.get_by_id(self.producto_id)
            if producto:
                producto.increase_stock(self.cantidad)
            
            # Actualizar estado
            return self.update_status('cancelado')
            
        except Exception as e:
            return False, f"Error al cancelar pedido: {str(e)}"
    
    def to_dict(self):
        """Convertir pedido a diccionario"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_total': float(self.precio_total),
            'estado': self.estado,
            'fecha_pedido': self.fecha_pedido.isoformat() if self.fecha_pedido else None
        }