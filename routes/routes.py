from flask import Blueprint
from controllers.usuario_controller import UsuarioController
from controllers.producto_controller import ProductoController
from controllers.pedido_controller import PedidoController

main = Blueprint('main', __name__)

# ==================== RUTAS DASHBOARD ====================
@main.route('/')
def index():
    """Dashboard principal con estadísticas"""
    try:
        # Obtener estadísticas de cada controller
        usuario_stats = UsuarioController.get_stats()
        producto_stats = ProductoController.get_stats()
        pedido_stats = PedidoController.get_stats()
        
        from flask import render_template
        return render_template('index.html',
                             usuarios=usuario_stats['total_usuarios'],
                             productos=producto_stats['total_productos'],
                             pedidos=pedido_stats['total_pedidos'])
    except Exception as e:
        from flask import render_template, flash
        flash(f'Error al cargar dashboard: {str(e)}', 'error')
        return render_template('index.html', usuarios=0, productos=0, pedidos=0)

# ==================== RUTAS USUARIOS ====================
@main.route('/usuarios')
def usuarios():
    """Mostrar página de usuarios"""
    return UsuarioController.index()

@main.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    """Crear nuevo usuario"""
    return UsuarioController.create()

@main.route('/usuarios/buscar')
def buscar_usuarios():
    """Buscar usuarios"""
    return UsuarioController.search()

# ==================== RUTAS PRODUCTOS ====================
@main.route('/productos')
def productos():
    """Mostrar página de productos"""
    return ProductoController.index()

@main.route('/productos/nuevo', methods=['POST'])
def nuevo_producto():
    """Crear nuevo producto"""
    return ProductoController.create()

@main.route('/productos/buscar')
def buscar_productos():
    """Buscar productos"""
    return ProductoController.search()

@main.route('/productos/categoria')
def productos_por_categoria():
    """Filtrar productos por categoría"""
    return ProductoController.get_by_category()

# ==================== RUTAS PEDIDOS ====================
@main.route('/pedidos')
def pedidos():
    """Mostrar página de pedidos"""
    return PedidoController.index()

@main.route('/pedidos/nuevo', methods=['POST'])
def nuevo_pedido():
    """Crear nuevo pedido"""
    return PedidoController.create()

@main.route('/pedidos/usuario')
def pedidos_por_usuario():
    """Ver pedidos de un usuario específico"""
    return PedidoController.get_by_user()

@main.route('/pedidos/actualizar-estado', methods=['POST'])
def actualizar_estado_pedido():
    """Actualizar estado de un pedido"""
    return PedidoController.update_status()

@main.route('/pedidos/cancelar', methods=['POST'])
def cancelar_pedido():
    """Cancelar un pedido"""
    return PedidoController.cancel()

# ==================== RUTAS API (Opcional) ====================
@main.route('/api/usuarios')
def api_usuarios():
    """API endpoint para usuarios"""
    from flask import jsonify
    try:
        from models.usuario_model import Usuario
        usuarios = Usuario.get_all()
        return jsonify([usuario.to_dict() for usuario in usuarios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/productos')
def api_productos():
    """API endpoint para productos"""
    from flask import jsonify
    try:
        from models.producto_model import Producto
        productos = Producto.get_all()
        return jsonify([producto.to_dict() for producto in productos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/pedidos')
def api_pedidos():
    """API endpoint para pedidos"""
    from flask import jsonify
    try:
        from models.pedido_model import Pedido
        pedidos = Pedido.get_all()
        return jsonify([pedido.to_dict() for pedido in pedidos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500