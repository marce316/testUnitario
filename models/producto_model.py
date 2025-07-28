from models import db
from models.base_model import BaseModel
from datetime import datetime
from sqlalchemy import Numeric
from decimal import Decimal

class Producto(BaseModel, db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con pedidos (comentada temporalmente para tests)
    # pedidos = db.relationship('Pedido', backref='producto', lazy=True)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'
    
    # Métodos específicos del modelo Producto
    @classmethod
    def create_product(cls, nombre, precio, descripcion=None, stock=0, categoria=None):
        """Crear un nuevo producto con validación"""
        try:
            # Validaciones
            if not nombre or len(nombre.strip()) < 2:
                return None, "El nombre debe tener al menos 2 caracteres"
            
            try:
                precio_decimal = Decimal(str(precio))
                if precio_decimal <= 0:
                    return None, "El precio debe ser mayor a 0"
            except:
                return None, "El precio no es válido"
            
            try:
                stock_int = int(stock)
                if stock_int < 0:
                    return None, "El stock no puede ser negativo"
            except (ValueError, TypeError):
                return None, "El stock debe ser un número entero válido"
            
            # Crear producto
            producto = cls(
                nombre=nombre.strip(),
                descripcion=descripcion.strip() if descripcion else None,
                precio=precio_decimal,
                stock=int(stock),
                categoria=categoria.strip() if categoria else None
            )
            
            success, message = producto.save()
            if success:
                return producto, "Producto creado exitosamente"
            else:
                return None, message
                
        except Exception as e:
            return None, f"Error inesperado: {str(e)}"
    
    @classmethod
    def get_by_category(cls, categoria):
        """Obtener productos por categoría"""
        try:
            return cls.query.filter_by(categoria=categoria).all()
        except Exception as e:
            print(f"Error al buscar por categoría: {e}")
            return []
    
    @classmethod
    def get_available_products(cls):
        """Obtener productos con stock disponible"""
        try:
            return cls.query.filter(cls.stock > 0).all()
        except Exception as e:
            print(f"Error al obtener productos disponibles: {e}")
            return []
    
    @classmethod
    def search_by_name(cls, nombre):
        """Buscar productos por nombre"""
        try:
            return cls.query.filter(cls.nombre.ilike(f'%{nombre}%')).all()
        except Exception as e:
            print(f"Error al buscar por nombre: {e}")
            return []
    
    def reduce_stock(self, cantidad):
        """Reducir stock del producto"""
        if self.stock >= cantidad:
            self.stock -= cantidad
            return self.update(stock=self.stock)
        else:
            return False, "Stock insuficiente"
    
    def increase_stock(self, cantidad):
        """Aumentar stock del producto"""
        self.stock += cantidad
        return self.update(stock=self.stock)
    
    def is_available(self, cantidad=1):
        """Verificar si hay stock suficiente"""
        return self.stock >= cantidad
    
    def to_dict(self):
        """Convertir producto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),
            'stock': self.stock,
            'categoria': self.categoria,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }