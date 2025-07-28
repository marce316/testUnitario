from flask import request, flash, redirect, url_for, render_template
from models.pedido_model import Pedido
from models.usuario_model import Usuario
from models.producto_model import Producto

class PedidoController:
    """Controller para manejar la lógica de pedidos"""
    
    @staticmethod
    def index():
        """Mostrar lista de pedidos"""
        try:
            pedidos = Pedido.get_orders_with_details()
            usuarios = Usuario.get_all()
            productos = Producto.get_available_products()
            
            return render_template('pedidos.html', 
                                 pedidos=pedidos, 
                                 usuarios=usuarios, 
                                 productos=productos)
        except Exception as e:
            flash(f'Error al cargar pedidos: {str(e)}', 'error')
            return render_template('pedidos.html', 
                                 pedidos=[], 
                                 usuarios=[], 
                                 productos=[])
    
    @staticmethod
    def create():
        """Crear un nuevo pedido"""
        if request.method == 'POST':
            # Obtener datos del formulario
            usuario_id = request.form.get('usuario_id')
            producto_id = request.form.get('producto_id')
            cantidad = request.form.get('cantidad')
            
            # Validar datos básicos
            try:
                usuario_id = int(usuario_id) if usuario_id else None
                producto_id = int(producto_id) if producto_id else None
                cantidad = int(cantidad) if cantidad else None
            except ValueError:
                flash('Datos inválidos en el formulario', 'error')
                return redirect(url_for('main.pedidos'))
            
            # Crear pedido usando el modelo
            pedido, mensaje = Pedido.create_order(usuario_id, producto_id, cantidad)
            
            if pedido:
                flash(mensaje, 'success')
            else:
                flash(mensaje, 'error')
            
            return redirect(url_for('main.pedidos'))
        
        # Si es GET, mostrar el formulario
        return PedidoController.index()
    
    @staticmethod
    def get_by_user():
        """Obtener pedidos de un usuario específico"""
        usuario_id = request.args.get('usuario_id')
        if usuario_id:
            try:
                usuario_id = int(usuario_id)
                pedidos = Pedido.get_by_user(usuario_id)
                usuario = Usuario.get_by_id(usuario_id)
                
                return render_template('pedidos_usuario.html', 
                                     pedidos=pedidos, 
                                     usuario=usuario)
            except ValueError:
                flash('ID de usuario inválido', 'error')
        
        return redirect(url_for('main.pedidos'))
    
    @staticmethod
    def update_status():
        """Actualizar estado de un pedido"""
        pedido_id = request.form.get('pedido_id')
        nuevo_estado = request.form.get('estado')
        
        if pedido_id and nuevo_estado:
            try:
                pedido_id = int(pedido_id)
                pedido = Pedido.get_by_id(pedido_id)
                
                if pedido:
                    success, mensaje = pedido.update_status(nuevo_estado)
                    if success:
                        flash(mensaje, 'success')
                    else:
                        flash(mensaje, 'error')
                else:
                    flash('Pedido no encontrado', 'error')
            except ValueError:
                flash('ID de pedido inválido', 'error')
        
        return redirect(url_for('main.pedidos'))
    
    @staticmethod
    def cancel():
        """Cancelar un pedido"""
        pedido_id = request.form.get('pedido_id')
        
        if pedido_id:
            try:
                pedido_id = int(pedido_id)
                pedido = Pedido.get_by_id(pedido_id)
                
                if pedido:
                    success, mensaje = pedido.cancel_order()
                    if success:
                        flash(mensaje, 'success')
                    else:
                        flash(mensaje, 'error')
                else:
                    flash('Pedido no encontrado', 'error')
            except ValueError:
                flash('ID de pedido inválido', 'error')
        
        return redirect(url_for('main.pedidos'))
    
    @staticmethod
    def get_stats():
        """Obtener estadísticas de pedidos"""
        pedidos = Pedido.get_all()
        return {
            'total_pedidos': len(pedidos),
            'pedidos_pendientes': len(Pedido.get_by_status('pendiente')),
            'pedidos_entregados': len(Pedido.get_by_status('entregado')),
            'revenue_total': sum([float(p.precio_total) for p in pedidos])
        }