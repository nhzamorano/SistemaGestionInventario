from flask import Flask, render_template, request, redirect,g,url_for,flash
from categorias import Categoria
from productos import Productos
from proveedores import Proveedores
from bodegas import Bodegas
from stock import Stock
import sqlite3


DATABASE = 'inventario.sqlite3'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def calcular_nevo_stock(tipo,stock,cantidad):
    print(f"desde fun{tipo}")
    if tipo == 'sumar':
        new_stock=stock+cantidad
    else:
        new_stock=stock-cantidad
        if new_stock < 0:
            new_stock=0
    return new_stock

categoria=Categoria()
producto = Productos()
proveedor = Proveedores()
bodega = Bodegas()
stk = Stock()

#Creamos la aplicacion
app = Flask(__name__)

app.secret_key = 'mysecretkey'
#Rutas
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/categorias')
def categorias():
    #cur = get_db().cursor()
    #cur.execute("SELECT * FROM categorias")  
    #categorias = cur.fetchall()
    lista=categoria.listar_categorias() 
    return render_template('categorias.html',categorias=lista)


@app.route('/add_categoria', methods=['POST'])
def add_categoria():
    if request.method == 'POST':
        nombre = request.form['name']
        descripcion = request.form['description']
        #cur = get_db().cursor()
        #cur.execute("INSERT INTO categorias (nombre,descripcion) VALUES (?, ?)",(nombre,descripcion))
        #get_db().commit()
        categoria.agregar_categorias(nombre,descripcion)
        flash('Categoria adicionada exitosamente')
        #categoria.agregar_categorias(name,description)
        return redirect(url_for('categorias'))

@app.route('/edit/<id>')
def get_categoria(id):
    #cur = get_db().cursor()
    #cur.execute("SELECT * FROM categorias WHERE id_categoria = {0}".format(id))
    #data = cur.fetchall()
    data=categoria.buscar_categoria(id)
    return render_template('edit_cat.html',categoria=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_categoria(id):
    if request.method == 'POST':
        nombre = request.form['name']
        descripcion = request.form['description']
        #cur = get_db().cursor()
        #cur.execute("UPDATE categorias SET nombre = ?, descripcion = ? WHERE id_categoria = ?", (nombre,descripcion,id))
        #get_db().commit()
        categoria.actualizar_categoria(nombre,descripcion,id)
        flash('Categoria actualizada exitosamente')
        return redirect(url_for('categorias'))

@app.route('/delete/<id>')
def delete_categoria(id):
    #cur = get_db().cursor()
    #cur.execute("DELETE FROM categorias WHERE id_categoria = {0}".format(int(id)))
    #get_db().commit()
    categoria.eliminar_categoria(id)
    flash('Categoria removida exitosamente')
    return redirect(url_for('categorias'))


#Modulo Productos
@app.route('/productos')
def productos():
    #cur = get_db().cursor()
    #cur.execute("SELECT p.id_producto,p.nombre,p.descripcion,p.stock,date(p.fecha_creacion),p.id_categoria, c.nombre FROM productos p  INNER JOIN categorias c ON p.id_categoria = c.id_categoria")  
    #data = cur.fetchall() 
    data = producto.listar_productos()
    #cargar categorias en el select html
    #cur1 = get_db().cursor()
    #cur1.execute("SELECT * FROM categorias")
    #cat = cur1.fetchall()
    lista=categoria.listar_categorias()
    return render_template('productos.html',productos=data,categorias=lista)


@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        stock = 0
        fecha = request.form['fecha']
        categoria = request.form['categoria']
        #cur = get_db().cursor()
        #cur.execute("INSERT INTO productos (nombre,descripcion,stock,fecha_creacion,id_categoria) VALUES (?,?,?,?,?)", (nombre,descripcion,stock,fecha,categoria))
        #get_db().commit()
        producto.agregar_productos(nombre,descripcion,stock,fecha,categoria)
        flash('Producto adicionado exitosamente')
        return redirect(url_for('productos'))
        #https://es.stackoverflow.com/questions/2193/sqlite3-no-da-fallo-al-insertar-referencia-inexistente

@app.route('/edit_prod/<id>')
def get_producto(id):
    #cur = get_db().cursor()
    #cur.execute("SELECT id_producto,nombre,descripcion,stock,date(fecha_creacion),id_categoria FROM productos WHERE id_producto = {0}".format(id))
    #data = cur.fetchall()
    data = producto.buscar_producto(id)
    resp=(data[0][5])
    cur1 = get_db().cursor()
    cur1.execute("SELECT id_categoria,nombre FROM categorias WHERE id_categoria = {0}".format(resp))
    cat = cur1.fetchall()
    #cat = categoria.buscar_categoria(resp)
    print(cat[0])
    #data=cat[0]
    cur1.execute("SELECT * FROM categorias")
    categorias =cur1.fetchall()
    print(cat)
    print(categorias)
    return render_template('edit_prod.html',producto=data[0],categorias=categorias,cat_actual=cat[0])

@app.route('/update_prod/<id>', methods=['POST'])
def update_producto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        stock = 0
        fecha = request.form['fecha']
        categoria = request.form['categoria']
        #id_cat=request.form['id_cat']
        #cur = get_db().cursor()
        #cur.execute("UPDATE productos SET nombre = ?,descripcion = ?, stock = ?, fecha_creacion = ?, id_categoria = ? WHERE id_producto = ?", (nombre,descripcion,stock,fecha,categoria,id))
        #get_db().commit()
        producto.actualizar_produto(nombre,descripcion,stock,fecha,categoria,id)
        flash('Producto actualizado exitosamente')        
        return redirect(url_for('productos'))

@app.route('/delete_prod/<id>')
def delete_prod(id):
    cur = get_db().cursor()
    cur.execute("DELETE FROM productos WHERE id_producto = {0}".format(id))
    get_db().commit()
    flash('Producto eliminado exitosamente')
    return redirect(url_for('productos'))

#Consultas y Reportes
@app.route('/consultar_productos')
def consultar_productos():
    data = producto.listar_productos()
    
    #print(data)
    return render_template('consulta_productos.html',productos = data)

@app.route('/consulta_producto_item/<id>')
def consulta_producto_item(id):
    #print(id)
    data = producto.consultar_producto(id)
    print(data)
    return render_template('consulta_productos.html',detalles=data)




#Proveedores
@app.route('/proveedores')
def proveedores():
    data=proveedor.listar_proveedores()
    if data == None:
        data="Vacio"
    return render_template('proveedores.html',proveedores=data)

@app.route('/add_proveedor', methods=['POST'])
def add_proveedor():
    if request.method == 'POST':
        nombre = request.form['name']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        fecha = request.form['fecha']
        proveedor.agregar_proveedor(nombre,direccion,telefono,fecha)
        flash("Proveedor agregado exitosamente")
        return redirect(url_for('proveedores'))

@app.route('/edit_proveedor/<id>')
def get_proveedor(id):
    data = proveedor.buscar_proveedor(id)
    return render_template('edit_proveedor.html',proveedor=data[0])

@app.route('/update_proveedor/<id>', methods=['POST'])
def update_proveedor(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        fecha = request.form['fecha']
        proveedor.actualizar_proveedor(nombre,direccion,telefono,fecha,id)
        flash('Proveedor actualizado exitosamente')
        return redirect(url_for('proveedores'))

@app.route('/delete_proveedor/<id>')
def delete_proveedor(id):
    proveedor.eliminar_proveedor(id)
    flash("Proveedor eliminado con exito")
    return redirect(url_for('proveedores'))

#Bodegas
@app.route('/bodegas')
def bodegas():
    data = bodega.listar_bodegas()
    return render_template('bodegas.html',bodegas=data)

@app.route('/add_bodega', methods=['POST'])
def add_bodega():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        capacidad = request.form['capacidad']
        fecha = request.form['fecha']
        bodega.agregar_bodegas(nombre,ubicacion,capacidad,fecha)
        flash('Bodega agregada exitosamente')
        return redirect(url_for('bodegas'))

@app.route('/edit_bodega/<id>')
def get_bodega(id):
    data = bodega.buscar_bodega(id)
    return render_template('edit_bodega.html',bodega=data[0])

@app.route('/update_bodega/<id>', methods=['POST'])
def update_bodega(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        capacidad = request.form['capacidad']
        fecha = request.form['fecha']
        bodega.actualizar_bodega(nombre,ubicacion,capacidad,fecha,id)
        flash('Bodega actualizada exitosamente')
        return redirect(url_for('bodegas'))

@app.route('/delete_bodega/<id>')
def delete_bodega(id):
    bodega.eliminar_bodega(id)
    flash('Bodega eliminada exitosamente')
    return redirect(url_for('bodegas'))

#Stock de productos
@app.route('/stock')
def stock():
    data=stk.listar_stock()
    print(data)
    productos = producto.listar_productos_nombre()
    proveedores = proveedor.listar_proveedores()
    return render_template('stock.html',productos=productos,proveedores=proveedores,datos=data)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    if request.method == 'POST':
        proveedor = request.form['proveedor']
        producto = request.form['producto']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        stk.agregar_stock(proveedor,producto,precio,cantidad,fecha)
        flash("Stock adicionado exitosamente")
        return redirect(url_for('stock'))

@app.route('/edit_stok/<id>')
def edit_stock(id):
    data = stk.buscar_stock(id)
    print(data)
    return render_template('manejo_stock.html',dato=data[0])

@app.route('/update_stock/<id>', methods=['POST'])
def update_stock(id):
    if request.method == 'POST':
        stock = int(request.form['stock_actual'])
        cantidad = int(request.form['cantidad'])
        tipo = request.form['tipo_operacion']
        new_stock = calcular_nevo_stock(tipo,stock,cantidad)
        stk.actualizar_stock(id,new_stock)
        flash("Stock actualizado exitosamente")
        return redirect(url_for('stock'))

@app.route('/total_stock')
def total_stock():
    total = stk.total_stock()
    print(total)
    return render_template('valor_stock.html',total=total[0])







@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Programa principal
if __name__ == '__main__':
    app.run(port=8000, debug=True)
