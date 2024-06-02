import sqlite3
class Bodegas:
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.sqlite3', check_same_thread=False)
        self.cursor = self.conexion.cursor()

    def listar_bodegas(self):
        self.cursor.execute("SELECT * FROM bodegas")
        self.bodegas = self.cursor.fetchall()
        return self.bodegas
    
    def listar_bodegas_nombre(self):
        self.cursor.execute("SELECT id_bodega,nombre FROM bodegas") 
        self.bodegas = self.cursor.fetchall()
        return self.bodegas

    def buscar_bodega_capacidad(self,bodega):
        self.cursor.execute("SELECT id_bodega,capacidad FROM bodegas WHERE id_bodega = {0}".format(bodega))
        return self.cursor.fetchall()

    def agregar_bodegas(self,nombre,ubicacion,capacidad,fecha):
        self.cursor.execute("INSERT INTO bodegas (nombre,ubicacion,capacidad,fecha) VALUES(?,?,?,?)",(nombre,ubicacion,capacidad,fecha))
        self.conexion.commit()
    
    def buscar_bodega(self,id):
        self.cursor.execute("SELECT * FROM bodegas WHERE id_bodega = {0}".format(id))
        self.data = self.cursor.fetchall()
        return self.data
    
    def actualizar_bodega(self,nombre,ubicacion,capacidad,fecha,id):
        self.cursor.execute("""
                UPDATE bodegas SET nombre = ?,
                ubicacion = ?,
                capacidad = ?,
                fecha = ?
                WHERE id_bodega = ?
                """,(nombre,ubicacion,capacidad,fecha,id))
        self.conexion.commit()
    
    def eliminar_bodega(self,id):
        self.cursor.execute("DELETE FROM bodegas WHERE id_bodega = {0}".format(id))
        self.conexion.commit()