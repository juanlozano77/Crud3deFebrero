
# -*- coding: utf-8 -*
import sqlite3
from PyQt5.QtWidgets import QMessageBox 

class consultas_db:
    """Clase para manejar las consultas a la base de datos."""

    def __init__(self, db_name="datos/datos.db"):
        self.db_name = db_name

    def _conectar(self):
        """Crea una conexión a la base de datos."""
        conexion = sqlite3.connect(self.db_name)
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def buscar_maximo(self, codigo):
        """Busca el stock máximo de un producto."""
        if codigo is None:
            return 0
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("SELECT stock FROM stock WHERE id = ?", (codigo,))
            return cur.fetchone()[0]
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al buscar máximo stock: {e}")  # Mostrar error en pantalla
            return 0
        finally:
            if conn:
                conn.close()

    def buscar_facturas(self, nombre_cliente):
        """Busca facturas por nombre de cliente."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            query = f'''SELECT a.numero, a.fecha, b.nombre, c.tipo, a.numero, a.total
                        FROM factura AS a
                        INNER JOIN clientes AS b ON a.id_cliente = b.codigo
                        INNER JOIN tipo_documentos AS c ON b.tipo_documento = c.codigo
                        WHERE b.nombre LIKE ?'''
            cur.execute(query, (f"%{nombre_cliente}%",))
            return cur.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al buscar facturas: {e}")  # Mostrar error en pantalla
            return []
        finally:
            if conn:
                conn.close()

    def buscar_clientes(self, nombre_cliente):
        """Busca clientes por nombre."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            query = f'''SELECT a.codigo, a.nombre, a.tipo_documento, b.tipo, a.numero, 
                        a.domicilio, a.cod_localidad, c.nombre, d.nombre
                        FROM clientes AS a
                        INNER JOIN tipo_documentos AS b ON a.tipo_documento = b.codigo
                        INNER JOIN localidad AS c ON a.cod_localidad = c.id_localidad
                        INNER JOIN provincia AS d ON c.id_provincia = d.id_provincia
                        WHERE a.nombre LIKE ?'''
            cur.execute(query, (f"%{nombre_cliente}%",))
            return cur.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al buscar clientes: {e}")  # Mostrar error en pantalla
            return []
        finally:
            if conn:
                conn.close()

    def buscar_localidad(self, nombre_localidad):
        """Busca localidad por nombre."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            query = f'''SELECT a.id_localidad, a.nombre, a.id_provincia, b.nombre
                        FROM localidad AS a
                        INNER JOIN provincia AS b ON a.id_provincia = b.id_provincia
                        WHERE a.nombre LIKE ?'''
            cur.execute(query, (f"%{nombre_localidad}%",))
            return cur.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al buscar localidades: {e}")  # Mostrar error en pantalla
            return []
        finally:
            if conn:
                conn.close()

    def buscar_provincia(self, nombre_provincia):
        """Busca provincia por nombre."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            query = f'''SELECT id_provincia,nombre
                        FROM provincia
                        WHERE nombre LIKE ?'''
            cur.execute(query, (f"%{nombre_provincia}%",))
            return cur.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al buscar provincias: {e}")  # Mostrar error en pantalla
            return []
        finally:
            if conn:
                conn.close()

    def buscar_documento(self, nombre_documento):
        """Busca documento por nombre."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            query = f'''SELECT codigo,tipo
                        FROM tipo_documentos
                        WHERE tipo LIKE ?'''
            cur.execute(query, (f"%{nombre_documento}%",))
            return cur.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al buscar documentos: {e}")  # Mostrar error en pantalla
            return []
        finally:
            if conn:
                conn.close()

    def obtener_clientes(self):
        """Obtiene todos los clientes."""
        try:
            conn = self._conectar()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT codigo, nombre FROM clientes")
            resultados = cur.fetchall()
            return {row['codigo']: row['nombre'] for row in resultados}
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al obtener clientes: {e}")  # Mostrar error en pantalla
            return {}
        finally:
            if conn:
                conn.close()

    def obtener_provincias(self):
        """Obtiene todas las provincias."""
        try:
            conn = self._conectar()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT id_provincia, nombre FROM provincia")
            resultados = cur.fetchall()
            return {row['id_provincia']: row['nombre'] for row in resultados}
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al obtener provincias: {e}")  # Mostrar error en pantalla
            return {}
        finally:
            if conn:
                conn.close()

    def obtener_articulos(self):
        """Obtiene todos los artículos."""
        try:
            conn = self._conectar()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT id, descripcion FROM stock")
            resultados = cur.fetchall()
            return {row['id']: row['descripcion'] for row in resultados}
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al obtener artículos: {e}")  # Mostrar error en pantalla
            return {}
        finally:
            if conn:
                conn.close()

    def obtener_tipos(self):
        """Obtiene todos los tipos de documentos."""
        try:
            conn = self._conectar()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT codigo, tipo FROM tipo_documentos")
            resultados = cur.fetchall()
            return {row['codigo']: row['tipo'] for row in resultados}
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al obtener tipos de documentos: {e}")  # Mostrar error en pantalla
            return {}
        finally:
            if conn:
                conn.close()

    def obtener_localidad(self):
        """Obtiene todas las localidades."""
        try:
            conn = self._conectar()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT id_localidad, nombre FROM localidad")
            resultados = cur.fetchall()
            return {row['id_localidad']: row['nombre'] for row in resultados}
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al obtener localidades: {e}")  # Mostrar error en pantalla
            return {}
        finally:
            if conn:
                conn.close()

    def buscar_productos(self, nombre_producto):
        """Busca todos los productos."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("SELECT id, descripcion, precio_venta, stock FROM stock")
            return cur.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al buscar productos: {e}")  # Mostrar error en pantalla
            return []
        finally:
            if conn:
                conn.close()

    def grabar_clientes(self, nombre, domicilio, id_documento, documento, id_localidad):
        """Graba un nuevo cliente."""
        try:
            
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO clientes (nombre, tipo_documento, numero, domicilio, cod_localidad) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (nombre, id_documento, documento, domicilio, id_localidad))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al grabar cliente: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()

    def modificar_cliente(self, codigo, nombre, domicilio, id_documento, documento, id_localidad):
        """Modifica un cliente existente."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("UPDATE clientes SET nombre = ?, tipo_documento = ?, numero = ?, domicilio = ?, "
                        "cod_localidad = ? WHERE codigo = ?",
                        (nombre, id_documento, documento, domicilio, id_localidad, codigo))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al modificar cliente: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()

    def grabar_stock(self, descripcion, stock, precio):
        """Graba un nuevo producto en stock."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO stock (descripcion, precio_venta, stock) VALUES (?, ?, ?)",
                        (descripcion, precio, stock))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al grabar stock: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()

    def grabar_factura(self, fecha, cliente, total):
        """Graba una nueva factura."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO factura (fecha, id_cliente, total) VALUES (?, ?, ?)",
                        (fecha, cliente, total))
            factura_id = cur.lastrowid
            conn.commit()
            return factura_id
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al grabar factura: {e}")  # Mostrar error en pantalla
            return None
        finally:
            if conn:
                conn.close()

    def grabar_item_factura(self, numero_factura, codigo, cantidad, precio):
        """Graba un item en la factura."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO item_factura (id_factura, id_item, cantidad, precio) "
                        "VALUES (?, ?, ?, ?)",
                        (numero_factura, codigo, cantidad, precio))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al grabar item de factura: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()

    def actualizar_stock(self,codigo, cantidad):
        """Actualiza el stock restando la cantidad especificada al stock actual."""
        try:
            # Conectar a la base de datos
            conn = self._conectar()  # Asegúrate de tener definida esta función en tu clase
            cur = conn.cursor()
        
            # Consultar el stock actual del producto
            cur.execute("SELECT stock FROM stock WHERE id = ?", (codigo,))
            resultado = cur.fetchone()
        
            if resultado is None:
                QMessageBox.warning(None, "Error", "No se encontró el producto con el código especificado.")
                return
        
            stock_actual = resultado[0]
        
            # Calcular el nuevo stock
            nuevo_stock = stock_actual - cantidad
        
            if nuevo_stock < 0:
                QMessageBox.warning(None, "Error", "No hay suficiente stock para realizar la operación.")
                return
        
            # Actualizar el stock en la base de datos
            cur.execute("UPDATE stock SET stock = ? WHERE id = ?", (nuevo_stock, codigo))
        
            # Confirmar los cambios
            conn.commit()
            QMessageBox.information(None, "Éxito", "Stock actualizado con éxito.")
        
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al actualizar el stock: {e}")
        finally:
            # Cerrar la conexión a la base de datos
            if conn:
                conn.close()


    def modificar_stock(self, descripcion, stock, precio, codigo):
        """Modifica un producto en stock."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("UPDATE stock SET descripcion = ?, precio_venta = ?, stock = ? WHERE id = ?",
                        (descripcion, precio, stock, codigo))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al modificar stock: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
                
    def grabar_provincia(self, nombre):
        """Graba una nueva provincia"""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO provincia (nombre) VALUES (?)", (nombre,))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al grabar provincia: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
                
    def modificar_provincia(self, codigo,nombre):
        """Modifica una provincia"""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("UPDATE provincia SET nombre = ? WHERE id_provincia = ?",
                        (nombre, codigo))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al modificar provincia: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
    def borrar_provincia(self, codigo):
        """Borra una localidad de la base de datos."""
        
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM provincia WHERE id_provincia = {codigo}")
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al borrar provincia: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
                
    def grabar_localidad(self, nombre, id_provincia):
        """Graba una nueva localidad"""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO localidad (nombre, id_provincia) "
                        "VALUES (?, ?)",
                        (nombre, id_provincia))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al grabar localidad: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
                
    def modificar_localidad(self, codigo,nombre,id_provincia):
        """Modifica una localidad"""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("UPDATE localidad SET nombre = ?, id_provincia = ? WHERE id_localidad = ?",
                        (nombre, id_provincia,codigo))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al modificar localidad: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
    def borrar_localidad(self, codigo):
        """Borra una localidad de la base de datos."""
        
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM localidad WHERE id_localidad = {codigo}")
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al borrar localidad: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()                

    def grabar_documento(self, nombre):
        """Graba una nuevo documento"""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO tipo_documentos (tipo) VALUES (?)", (nombre,))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al grabar documento: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
                
    def modificar_documento(self, codigo,nombre):
        """Modifica una documento"""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute("UPDATE tipo_documentos SET tipo = ? WHERE codigo = ?",
                        (nombre, codigo))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al modificar documento: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
    def borrar_documento(self, codigo):
        """Borra un documento de la base de datos."""
        
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM tipo_documentos WHERE codigo = {codigo}")
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al borrar documento: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()                

    def obtener_precio(self, codigo):
        """Obtiene el precio de un producto."""
        try:
            conn = self._conectar()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT precio_venta FROM stock WHERE id = ?", (codigo,))
            resultado = cur.fetchone()
            return resultado["precio_venta"] if resultado else None
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al obtener precio: {e}")  # Mostrar error en pantalla
            return None
        finally:
            if conn:
                conn.close()

    def obtener_datos_factura(self, cod_factura):
        """Obtiene los datos de una factura."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            query = f'''SELECT a.fecha, b.nombre, a.total 
                        FROM factura AS a 
                        INNER JOIN clientes AS b ON a.id_cliente = b.codigo 
                        WHERE a.numero = ?'''
            cur.execute(query, (cod_factura,))
            return cur.fetchone()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al obtener datos de la factura: {e}")  # Mostrar error en pantalla
            return None
        finally:
            if conn:
                conn.close()

    def obtener_items_factura(self, cod_factura):
        """Obtiene los items de una factura."""
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            query = f'''SELECT b.descripcion, a.cantidad, a.precio, (a.cantidad * a.precio) AS subtotal 
                        FROM item_factura AS a 
                        INNER JOIN stock AS b ON b.id = a.id_item
                        WHERE a.id_factura = ?'''
            cursor.execute(query, (cod_factura,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al obtener items de la factura: {e}")  # Mostrar error en pantalla
            return []
        finally:
            if conn:
                conn.close()

    def borrar_cliente(self, codigo):
        """Borra un cliente de la base de datos."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM clientes WHERE codigo = {codigo}")
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al borrar cliente: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()

    def borrar_producto(self, codigo):
        """Borra un producto de la base de datos."""
        try:
            conn = self._conectar()
            cur = conn.cursor()
            cur.execute(f"DELETE FROM stock WHERE id = {codigo}")
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Error de Base de Datos", f"Error al borrar producto: {e}")  # Mostrar error en pantalla
        finally:
            if conn:
                conn.close()
                
