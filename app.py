from flask import Flask, render_template, request, redirect,g,url_for,flash
from categorias import Categoria
from productos import Productos
from proveedores import Proveedores
from bodegas import Bodegas
from stock import Stock
from gestion_bodega import MovimientoBodega
#from producto_bodega import ProductoInBdega
import sqlite3


DATABASE = 'inventario.sqlite3'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def calcular_nevo_stock(tipo,stock,cantidad):
    #print(f"desde fun{tipo}")
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
movimiento = MovimientoBodega()
#productobode = ProductoInBdega()

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

@app.route('/listar_cateorias')
def listar_categorias():
    lista=categoria.listar_categorias()
    return render_template('consulta_categorias.html',categorias=lista)

@app.route('/consultar_categoria_item/<id>')
def consulta_categoria_item(id):
    data=categoria.consultar_categoria(id)
    #print(data)
    return render_template('consulta_categorias.html',detalles=data)


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
    #print(cat[0])
    #data=cat[0]
    cur1.execute("SELECT * FROM categorias")
    categorias =cur1.fetchall()
    #print(cat)
    #print(categorias)
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
    #print(data)
    return render_template('consulta_productos.html',detalles=data)

@app.route('/test')
def test():
    data = producto.listar_productos_nombre()
    #print(data)
    return render_template('test.html',productos=data)

@app.route('/buscar_prod/<id>',methods=['POST'])
def buscar_prod(id):
    if request.method == 'POST':
        #print(id)
        data = producto.consultar_producto(id)
        #print(id)
        return render_template('test1.html',detalles=data)

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

@app.route('/listar_proveedores')
def listar_proveedores():
    data = proveedor.listar_proveedores()
    return render_template('consulta_proveedores.html',proveedores=data)

@app.route('/consultar_proveedor_item/<id>')
def consultar_proveedor_item(id):
    data=proveedor.consultar_proveedor(id)
    #print(data)
    return render_template('consulta_proveedores.html',detalles=data)

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

#Movimiento de bodega
@app.route('/gestion_bodega_producto')
def gestion_bodega_producto():
    data=movimiento.listar_movimiento()
    bdga = bodega.listar_bodegas()
    prod = stk.listar_producto_stock_nombre()
    #print(data)
    return render_template('movimiento_bodega.html',movimientos=data,bodegas=bdga,productos=prod)

@app.route('/adicionar_mvto_bodega_producto', methods = ['POST'])
def adicionar_mvto_bodega_producto():
    if request.method == 'POST':
        bdga = request.form['bodega']
        prdcto = request.form['producto']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        """
        1. sumar la cantidad de producto almacenados en esa bodega
        2. buscar la capacida de la bodega
        3. sumamos la cantidad que llega del formulario a la cantidad existente
        4.  comparamos si exede la capacidad mostrar mensaje no grabar
        """
        cant = movimiento.consultar_cantidad_almacenada(bdga)
        if cant:
            cant_almacenada = cant[0][0]
        else:
            cant_almacenada=0
        capacidad_bodega = bodega.buscar_bodega_capacidad(bdga)
        capacidad_bodega = capacidad_bodega[0][1]
        if (int(cant_almacenada) + int(cantidad))>= int(capacidad_bodega):
            flash("La cantidad excede la capacida de la bodega")
        else:
            ext_bod = movimiento.buscar_bodeda_en_bodega(bdga)
            if ext_bod:
                ext_prod = movimiento.buscar_producto_en_bodega(bdga,prdcto)
                if ext_prod:
                    stock_actual = ext_prod[0][0]
                    new_stock = int(stock_actual) + int(cantidad)
                    movimiento.actualizar_producto_bodega(bdga,prdcto,new_stock)
                else:
                    movimiento.add_in_pbodega(bdga,prdcto,cantidad,fecha)
            else:
                movimiento.add_in_pbodega(bdga,prdcto,cantidad,fecha)
        return redirect(url_for('gestion_bodega_producto'))

@app.route('/edit_producto_bodega/<idp>/<idb>')
def eliminar_producto_bodega(idp,idb):
    """
    1. Buscar el producto en movimiento de bodeda
    2. cargar datos en formulario
    ----
    2. sumar cantidad de ese producto agrupando por producto y bodega
    3. verificar si cantidad a retirar sobrepasa el stock de ese producto
    """
    data = movimiento.buscar_producto_bodega(idp,idb)
    stock_producto = data[0][2]
    return render_template('retirar_producto_bodega.html',dato=data[0])

@app.route('/update_producto_bodega', methods=['POST'])
def update_producto_bodega():
    if request.method == 'POST':
        id_bodega=request.form['id_bodega']
        id_producto=request.form['id_producto']
        stock_actual=request.form['stock']
        stock_actual = int(stock_actual)
        cant_retirar=request.form['cant_retirar']
        cant_retirar=int(cant_retirar)
        #print(f"{id_bodega} {id_producto} {stock_actual} {cant_retirar}")
        if cant_retirar > stock_actual or (stock_actual - cant_retirar <= 0):
            flash("El stock  en la bodga no puede quedar en 0 ")
        else:
            nuevo_stock = stock_actual - cant_retirar
            movimiento.actualizar_producto_bodega(id_bodega,id_producto,nuevo_stock)
            flash("El stock de la bodega se actualizo exitosamente")
        return redirect(url_for('gestion_bodega_producto'))

@app.route('/consultar_disponibilidad_producto/<idp>')
def consultar_disponibilidad_producto(idp):
    print(idp)
    cons = movimiento.consultar_disponibilidad_producto_en_bodega(idp)
    print(cons)
    return render_template('mostrar_disp_prod.html', datos=cons)

@app.route('/listar_bodegas')
def listar_bodegas():
    lst = movimiento.listar_informacion_bodega()
    mvto = movimiento.listar_mvto_bodega_producto()
    print(lst)
    print(mvto)
    return render_template('listado_mvto_bodega.html',listado=lst,datos=mvto)


#Stock de productos
@app.route('/stock')
def stock():
    data=stk.listar_stock()
    productos = producto.listar_productos_nombre()
    proveedores = proveedor.listar_proveedores()
    bodegas = bodega.listar_bodegas_nombre()
    return render_template('stock.html',productos=productos,proveedores=proveedores,datos=data,bodegas=bodegas)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    if request.method == 'POST':
        proveedor = request.form['proveedor']
        producto = request.form['producto']
        bodega = request.form['bodega']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        stk.agregar_stock(proveedor,producto,precio,cantidad,fecha)
        #Adicionamos mvto a movimiento de bodega
        movimiento.add_in_pbodega(bodega,producto,cantidad,fecha)
        flash("Stock adicionado exitosamente")
        return redirect(url_for('stock'))

@app.route('/edit_stok/<id>')
def edit_stock(id):
    data = stk.buscar_stock(id)
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

@app.route('/eliminar_mvto_producto/<id>')
def eliminar_mvto_producto(id):
    dato=movimiento.eliminar_mvto_bodega(id)
    dato1=stk.eliminar_producto_stock(id)
    flash('Movimiento de producto y bodega eliminada exitosamente')
    return redirect(url_for('stock'))

@app.route('/total_stock')
def total_stock():
    total = stk.total_stock()
    return render_template('valor_stock.html',total=total[0])

@app.route('/totales_stock')
def totales_stock():
    total=stk.total_stock()
    total_cat = stk.total_stock_categoria()
    total_prov = stk.total_stock_proveedor()
    return render_template('totales_stock.html',total=total[0],total_cat=total_cat,total_prov=total_prov)











@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Programa principal
if __name__ == '__main__':
    app.run(port=8000, debug=True)
