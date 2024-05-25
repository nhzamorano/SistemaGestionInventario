import sqlite3
class Stock:
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.sqlite3', check_same_thread=False)
        self.cursor = self.conexion.cursor()
    
    def listar_stock(self):  
        self.cursor.execute("""
            SELECT pp.id,p.id_producto,p.nombre,pr.id_proveedor,pr.nombre,pp.precio,pp.cantidad,pp.fecha FROM productos p, proveedores pr  INNER JOIN proveedor_producto pp ON pp.id_proveedor = pr.id_proveedor AND pp.id_producto = p.id_producto
        """)
        self.stok = self.cursor.fetchall()
        return self.stok

    def actualizar_stock(self,idpp,stock):
        self.cursor.execute("UPDATE proveedor_producto SET cantidad = ? WHERE id=?",(stock,idpp))
        self.conexion.commit()

    def agregar_stock(self,id_proveedor,id_producto,precio,cantidad,fecha):
        self.cursor.execute("INSERT INTO proveedor_producto (id_proveedor,id_producto,precio,cantidad,fecha) VALUES (?,?,?,?,?)",(id_proveedor,id_producto,precio,cantidad,fecha))
        self.conexion.commit()
    
    def buscar_stock(self,id):
        self.cursor.execute("""
            SELECT pp.id,p.id_producto,p.nombre,pr.id_proveedor,pr.nombre,pp.precio,pp.cantidad,pp.fecha FROM productos p, proveedores pr  INNER JOIN proveedor_producto pp ON pp.id_proveedor = pr.id_proveedor AND pp.id_producto = p.id_producto WHERE pp.id = ?
        """,(id,))
        self.data = self.cursor.fetchall()
        return self.data
    
    def total_stock(self):
        self.cursor.execute("SELECT SUM(cantidad) AS cant,SUM(precio*cantidad) AS total FROM proveedor_producto")
        self.data= self.cursor.fetchall()
        return self.data


