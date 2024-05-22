import sqlite3

class Create_db:
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.sqlite3')
        self.cursor = self.conexion.cursor()
    
    
    def Crear_Tablas(self):
        resp = input("Desea crear la estructura de la base de datos, se elliminaran todos los datos existentes, <S/N>: ")
        if resp.upper() == 'S':
            print("Creando estructura de la base de datos INVETARIOS")
            print()
            print("Creando tabala categorias ...")
            self.cursor.execute("""
                DROP TABLE IF EXISTS categorias;
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias(
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT
                );
            """)
            print()
            print("Creando tabala productos ...")
            self.cursor.execute("""
                DROP TABLE IF EXISTS productos;
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos(
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                stock INTEGER NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                id_categoria INTEGER NOT NULL,
                foreign key(id_categoria) references categorias(id_categoria)
                );
            """)
            print()
            print("Creando tabala proveedores ...")
            self.cursor.execute("""
                DROP TABLE IF EXISTS proveedores;
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS preveedores(
                id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            print()
            print("Creando tabala bodegas ...")
            self.cursor.execute("""
                DROP TABLE IF EXISTS bodegas;
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bodegas(
                id_bodega INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                ubicacion TEXT NOT NULL,
                capacidad INTEGER NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            print()
            print("Creando tabala proveedor_producto ...")
            self.cursor.execute("""
                DROP TABLE IF EXISTS proveedor_producto;
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS preveedor_producto(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_proveedor INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                precio INTEGER NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                foreign key(id_proveedor) references preveedores(id_proveedor),
                foreign key(id_producto) references productos(id_producto)
                );
            """)

            print()
            print("Creando tabala bodega_producto ...")
            self.cursor.execute("""
                DROP TABLE IF EXISTS bodega_producto;
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bodega_producto(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_bodega INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_salida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                foreign key(id_bodega) references bodegas(id_bodega),
                foreign key(id_producto) references productos(id_producto)
                );
            """)
    

db=Create_db()
db.Crear_Tablas()
