import sqlite3

class Productos:
    def __init__(self):
        #PRAGMA foreign_keys=ON
        self.conexion = sqlite3.connect('inventario.sqlite3',check_same_thread=False)
        self.cursor = self.conexion.cursor()
    
    
    def listar_productos(self):
        self.cursor.execute("SELECT p.id_producto,p.nombre,p.descripcion,p.stock,date(p.fecha_creacion),p.id_categoria, c.nombre FROM productos p  INNER JOIN categorias c ON p.id_categoria = c.id_categoria")  
        self.productos = self.cursor.fetchall()
        return self.productos

    def listar_productos_nombre(self):
        self.cursor.execute("SELECT id_producto,nombre FROM productos")
        self.data = self.cursor.fetchall()
        return self.data

    def buscar_stock(self,id):
        self.cursor.execute("SELECT id_producto,nombre,stock FROM productos WHERE id_producto = ?",(id,))
        self.data = self.cursor.fetchall()
        return self.data

    def agregar_productos(self,nombre,descripcion,stock,fecha,categoria):
        self.cursor.execute("INSERT INTO productos (nombre,descripcion,stock,fecha_creacion,id_categoria) VALUES (?,?,?,?,?)", (nombre,descripcion,stock,fecha,categoria))
        self.conexion.commit()
    
    def buscar_producto(self,id):
        self.cursor.execute("SELECT id_producto,nombre,descripcion,stock,date(fecha_creacion),id_categoria FROM productos WHERE id_producto = {0}".format(id))
        self.data = self.cursor.fetchall()
        return self.data   

    def actualizar_produto(self,nombre,descripcion,stock,fecha,categoria,id):
        self.cursor.execute("UPDATE productos SET nombre = ?,descripcion = ?, stock = ?, fecha_creacion = ?, id_categoria = ? WHERE id_producto = ?", (nombre,descripcion,stock,fecha,categoria,id))
        self.conexion.commit()
    
    def actualizar_stock(self,id,new_stock):
        self.cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?",(new_stock,id))
        self.conexion.commit()    

    def eliminar_producto(self,id):
        self.cursor.execute("DELETE FROM productos WHERE id_producto = {0}".format(id))
        self.conexion.commit()
    
    def consultar_producto(self,id):
        self.cursor.execute("""
            SELECT p.id_producto,p.nombre,
            p.descripcion, p.id_categoria, 
            c.nombre, pr.id_proveedor,
            pr.nombre,pp.id_proveedor,
            pp.id_producto,pp.precio,
            pp.cantidad FROM productos p, categorias c, proveedores pr   
            INNER JOIN proveedor_producto pp 
            ON p.id_categoria = c.id_categoria
            AND p.id_producto = pp.id_producto
            AND pr.id_proveedor = pp.id_proveedor
            WHERE p.id_producto = ?
            """,(id,))
        self.data = self.cursor.fetchall()
        return self.data  
