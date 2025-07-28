from flask import request, flash, redirect, url_for, render_template
from models.producto_model import Producto

class ProductoController:
    """Controller para manejar la lógica de productos"""
    
    @staticmethod
    def index():
        """Mostrar lista de productos"""
        try:
            productos = Producto.get_all()
            return render_template('productos.html', productos=productos)
        except Exception as e:
            flash(f'Error al cargar productos: {str(e)}', 'error')
            return render_template('productos.html', productos=[])
    
    @staticmethod  # <- Ahora con 4 espacios
    def create():  # <- Ahora con 4 espacios
        """Crear un nuevo producto"""
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            precio = request.form.get('precio', '0')
            stock = request.form.get('stock', '0')
            categoria = request.form.get('categoria', '').strip()
            
            # Validar y convertir tipos ANTES de pasar al modelo
            try:
                precio_float = float(precio) if precio else 0
                stock_int = int(stock) if stock else 0
            except ValueError:
                flash('Precio y stock deben ser números válidos', 'error')
                return redirect(url_for('main.productos'))
            
            # Crear producto usando el modelo
            producto, mensaje = Producto.create_product(
                nombre=nombre,
                precio=precio_float,
                descripcion=descripcion,
                stock=stock_int,
                categoria=categoria
            )
            
            if producto:
                flash(mensaje, 'success')
                return redirect(url_for('main.productos'))
            else:
                flash(mensaje, 'error')
                return redirect(url_for('main.productos'))
        
        # Si es GET, mostrar el formulario
        return ProductoController.index()
    
    @staticmethod
    def search():
        """Buscar productos por nombre"""
        query = request.args.get('q', '').strip()
        if query:
            productos = Producto.search_by_name(query)
            flash(f'Se encontraron {len(productos)} producto(s)', 'info')
        else:
            productos = Producto.get_all()
        
        return render_template('productos.html', productos=productos, search_query=query)
    
    @staticmethod
    def get_available():
        """Obtener productos disponibles para pedidos"""
        return Producto.get_available_products()
    
    @staticmethod
    def get_by_category():
        """Obtener productos por categoría"""
        categoria = request.args.get('categoria', '')
        if categoria:
            productos = Producto.get_by_category(categoria)
        else:
            productos = Producto.get_all()
        
        return render_template('productos.html', productos=productos, categoria_filtro=categoria)
    
    @staticmethod
    def get_stats():
        """Obtener estadísticas de productos"""
        productos = Producto.get_all()
        return {
            'total_productos': len(productos),
            'productos_sin_stock': len([p for p in productos if p.stock == 0]),
            'valor_total_inventario': sum([float(p.precio) * p.stock for p in productos])
        }