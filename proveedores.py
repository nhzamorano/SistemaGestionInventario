import sqlite3
class Proveedores:
    def __init__(self):
        #PRAGMA foreign_keys=ON
        self.conexion = sqlite3.connect('inventario.sqlite3',check_same_thread=False)
        self.cursor = self.conexion.cursor()

    def listar_proveedores(self):
        self.cursor.execute("SELECT * FROM proveedores")
        self.proveedores = self.cursor.fetchall()
        return self.proveedores
    
    def agregar_proveedor(self,nombre,direccion,telefono,fecha):
        self.cursor.execute("INSERT INTO proveedores(nombre,direccion,telefono,fecha_creacion) VALUES(?,?,?,?)",(nombre,direccion,telefono,fecha))
        self.conexion.commit()
    
    def buscar_proveedor(self,id):
        self.cursor.execute("SELECT id_proveedor,nombre,direccion,telefono,fecha_creacion FROM proveedores WHERE id_proveedor = {0}".format(id))
        self.data = self.cursor.fetchall()
        return self.data
    
    def actualizar_proveedor(self,nombre,direccion,telefono,fecha,id):
        self.cursor.execute("""
                UPDATE proveedores 
                SET nombre = ?,
                direccion = ?,
                telefono = ?,
                fecha_creacion = ? 
                WHERE id_proveedor = ?""",(nombre,direccion,telefono,fecha,id))
        self.conexion.commit()

    def eliminar_proveedor(self,id):
        self.cursor.execute("DELETE FROM proveedores WHERE id_proveedor = {0}".format(id))
        self.conexion.commit()
    

    def consultar_proveedor(self,id):
        self.cursor.execute("""
            SELECT pr.id_proveedor,pr.nombre,pr.direccion,pr.telefono,
            pp.id_proveedor, pp.id_producto, p.nombre 
            FROM proveedores pr, proveedor_producto pp  
            INNER JOIN productos p 
            ON pr.id_proveedor = pp.id_proveedor
            AND pp.id_producto = p.id_producto
            WHERE pr.id_proveedor = ?
            """,(id,))
        self.data = self.cursor.fetchall()
        return self.data  