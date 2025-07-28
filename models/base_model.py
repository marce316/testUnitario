from models import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class BaseModel:
    """Clase base para todos los modelos con operaciones CRUD comunes"""
    
    @classmethod
    def get_all(cls):
        """Obtener todos los registros"""
        try:
            return cls.query.all()
        except SQLAlchemyError as e:
            print(f"Error al obtener registros: {e}")
            return []
    
    @classmethod
    def get_by_id(cls, id):
        """Obtener un registro por ID"""
        try:
            return cls.query.get(id)
        except SQLAlchemyError as e:
            print(f"Error al obtener registro por ID: {e}")
            return None
    
    @classmethod
    def count(cls):
        """Contar total de registros"""
        try:
            return cls.query.count()
        except SQLAlchemyError as e:
            print(f"Error al contar registros: {e}")
            return 0
    
    def save(self):
        """Guardar el registro actual"""
        try:
            db.session.add(self)
            db.session.commit()
            return True, "Registro guardado exitosamente"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al guardar: {str(e)}"
    
    def delete(self):
        """Eliminar el registro actual"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True, "Registro eliminado exitosamente"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar: {str(e)}"
    
    def update(self, **kwargs):
        """Actualizar campos del registro"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True, "Registro actualizado exitosamente"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al actualizar: {str(e)}"