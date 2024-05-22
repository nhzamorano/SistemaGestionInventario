import sqlite3
class Categoria:
    def __init__(self):
        #PRAGMA foreign_keys=ON
        self.conexion = sqlite3.connect('inventario.sqlite3',check_same_thread=False)
        self.cursor = self.conexion.cursor()
    
    def agregar_categorias(self,nombre,descripcion):
        self.cursor.execute("INSERT INTO categorias (nombre,descripcion) VALUES (?, ?)",(nombre,descripcion))
        self.conexion.commit()
        #self.conexion.close()
    
    def listar_categorias(self):
        self.conexion.row_factory = sqlite3.Row #modo diccionario
        self.cursor = self.conexion.cursor()
        self.cursor.execute("""
            SELECT * FROM categorias;
        """)
        self.categorias = self.cursor.fetchall()
        return self.categorias
    
    def buscar_categoria(self,id):
        self.cursor.execute("SELECT * FROM categorias WHERE id_categoria = {0}".format(id))
        self.data = self.cursor.fetchall()
        return self.data
    
    def actualizar_categoria(self,nombre,descripcion,id):
        self.cursor.execute("UPDATE categorias SET nombre = ?, descripcion = ? WHERE id_categoria = ?", (nombre,descripcion,id))
        self.conexion.commit()
    
    def eliminar_categoria(self,id):
        self.cursor.execute("DELETE FROM categorias WHERE id_categoria = {0}".format(id))
        self.conexion.commit()

