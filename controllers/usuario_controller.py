from flask import request, flash, redirect, url_for, render_template
from models.usuario_model import Usuario

class UsuarioController:
    """Controller para manejar la lógica de usuarios"""
    
    @staticmethod
    def index():
        """Mostrar lista de usuarios"""
        try:
            usuarios = Usuario.get_all()
            return render_template('usuarios.html', usuarios=usuarios)
        except Exception as e:
            flash(f'Error al cargar usuarios: {str(e)}', 'error')
            return render_template('usuarios.html', usuarios=[])
    
    @staticmethod
    def create():
        """Crear un nuevo usuario"""
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre = request.form.get('nombre', '').strip()
            email = request.form.get('email', '').strip()
            telefono = request.form.get('telefono', '').strip()
            
            # Crear usuario usando el modelo
            usuario, mensaje = Usuario.create_user(nombre, email, telefono)
            
            if usuario:
                flash(mensaje, 'success')
                return redirect(url_for('main.usuarios'))
            else:
                flash(mensaje, 'error')
                return redirect(url_for('main.usuarios'))
        
        # Si es GET, mostrar el formulario
        return UsuarioController.index()
    
    @staticmethod
    def search():
        """Buscar usuarios por nombre"""
        query = request.args.get('q', '').strip()
        if query:
            usuarios = Usuario.search_by_name(query)
            flash(f'Se encontraron {len(usuarios)} usuario(s)', 'info')
        else:
            usuarios = Usuario.get_all()
        
        return render_template('usuarios.html', usuarios=usuarios, search_query=query)
    
    @staticmethod
    def get_stats():
        """Obtener estadísticas de usuarios"""
        return {
            'total_usuarios': Usuario.count(),
            'usuarios_recientes': Usuario.query.order_by(Usuario.fecha_registro.desc()).limit(5).all()
        }