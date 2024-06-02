import sqlite3

class MovimientoBodega:
    def __init__(self):
        #PRAGMA foreign_keys=ON
        self.conexion = sqlite3.connect('inventario.sqlite3',check_same_thread=False)
        self.cursor = self.conexion.cursor()
    
    def listar_movimiento(self):
        self.cursor.execute("""
            SELECT bp.id_bodega,
                bp.id_producto,
                SUM(bp.cantidad) AS cant,
                bp.fecha_ingreso,
                bp.fecha_salida,
                b.nombre,
                p.nombre 
            FROM bodega_producto bp, bodegas b  
            INNER JOIN productos p 
            ON bp.id_bodega = b.id_bodega
            AND bp.id_producto = p.id_producto
            GROUP BY bp.id_bodega,bp.id_producto
            """)  
        self.movimiento = self.cursor.fetchall()
        return self.movimiento

    def add_in_pbodega(self,bodega,producto,cantidad,fecha):
        #print(f"bodega {bodega} producto {producto} cantidad {cantidad} ")
        self.cursor.execute(""" INSERT INTO bodega_producto (id_bodega,id_producto,cantidad,fecha_ingreso) VALUES(?,?,?,?)""",(bodega,producto,cantidad,fecha))
        self.conexion.commit()


    def consultar_cantidad_almacenada(self,bodega):
        self.cursor.execute("SELECT SUM(cantidad) AS cant FROM bodega_producto WHERE id_bodega = {0} GROUP BY id_bodega".format(bodega))
        return self.cursor.fetchall()

    def buscar_producto_bodega(self,idp,idb):
        self.cursor.execute(
            """SELECT bp.id_bodega,bp.id_producto,
            bp.cantidad,b.nombre,p.nombre 
            FROM bodega_producto bp, bodegas b 
            INNER JOIN productos p
            ON bp.id_bodega = b.id_bodega
            AND bp.id_producto = p.id_producto 
            WHERE bp.id_producto = {0}  AND bp.id_bodega = {1}
            GROUP by bp.id_bodega""".format(idp,idb))
        #print(id)
        return self.cursor.fetchall()

    def buscar_bodeda_en_bodega(self,idb):
        self.cursor.execute("SELECT id_bodega FROM bodega_producto WHERE id_bodega = {0}".format(idb))
        return self.cursor.fetchall()

    def buscar_producto_en_bodega(self,idb,idp):
        self.cursor.execute("SELECT cantidad FROM bodega_producto WHERE id_bodega = ? AND id_producto = ?",(idb,idp))
        return self.cursor.fetchall()

    def actualizar_producto_bodega(self,bodega,producto,cant):
        self.cursor.execute("UPDATE bodega_producto SET cantidad = ? WHERE id_bodega = ? AND id_producto = ?",(cant,bodega,producto))
        self.conexion.commit()

    def consultar_disponibilidad_producto_en_bodega(self,idp):
        self.cursor.execute("""
            SELECT bp.id_bodega,bp.id_producto,
            bp.cantidad,b.nombre,p.nombre 
            FROM bodega_producto bp, bodegas b 
            INNER JOIN productos p
            ON bp.id_bodega = b.id_bodega
            AND bp.id_producto = p.id_producto
            WHERE bp.id_producto = {0}""".format(idp))
        return self.cursor.fetchall()

    def eliminar_mvto_bodega(self,id):
        self.cursor.execute("DELETE  FROM bodega_producto WHERE id_producto = {0}".format(id))
        self.conexion.commit()
    
    def listar_informacion_bodega(self):
        #, incluyendo su nombre, ubicación, capacidad máxima y la lista de productos almacenados
        self.cursor.execute("""
            SELECT DISTINCT bp.id_bodega,b.nombre,
                b.ubicacion,b.capacidad 
                FROM bodega_producto bp
                INNER JOIN bodegas b
                ON bp.id_bodega = b.id_bodega""")
        return self.cursor.fetchall()
    
    def listar_mvto_bodega_producto(self):
        self.cursor.execute("""
            SELECT DISTINCT bp.id_bodega,
            bp.id_producto,p.nombre 
            FROM bodega_producto bp, bodegas b
            INNER JOIN productos p
            ON bp.id_bodega = b.id_bodega
            AND bp.id_producto = p.id_producto
            """)
        return self.cursor.fetchall()