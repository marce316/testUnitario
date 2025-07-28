from models import db
from models.base_model import BaseModel
from datetime import datetime
from sqlalchemy import Numeric
from sqlalchemy.exc import IntegrityError

class Usuario(BaseModel, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con pedidos
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)
    
    def __repr__(self):
        return f'<Usuario {self.nombre}>'
    
    # Métodos específicos del modelo Usuario
    @classmethod
    def create_user(cls, nombre, email, telefono=None):
        """Crear un nuevo usuario con validación"""
        try:
            # Validaciones
            if not nombre or len(nombre.strip()) < 2:
                return None, "El nombre debe tener al menos 2 caracteres"
            
            if not email or '@' not in email:
                return None, "El email no es válido"
            
            # Verificar si el email ya existe
            if cls.get_by_email(email):
                return None, "El email ya está registrado"
            
            # Crear usuario
            usuario = cls(
                nombre=nombre.strip(),
                email=email.strip().lower(),
                telefono=telefono.strip() if telefono else None
            )
            
            success, message = usuario.save()
            if success:
                return usuario, "Usuario creado exitosamente"
            else:
                return None, message
                
        except Exception as e:
            return None, f"Error inesperado: {str(e)}"
    
    @classmethod
    def get_by_email(cls, email):
        """Buscar usuario por email"""
        try:
            return cls.query.filter_by(email=email.lower()).first()
        except Exception as e:
            print(f"Error al buscar por email: {e}")
            return None
    
    @classmethod
    def search_by_name(cls, nombre):
        """Buscar usuarios por nombre (búsqueda parcial)"""
        try:
            return cls.query.filter(cls.nombre.ilike(f'%{nombre}%')).all()
        except Exception as e:
            print(f"Error al buscar por nombre: {e}")
            return []
    
    def get_pedidos(self):
        """Obtener todos los pedidos del usuario"""
        return self.pedidos
    
    def to_dict(self):
        """Convertir usuario a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }