# -*- coding: utf-8 -*
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QDialog, QVBoxLayout,QLabel,QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ventana import Ui_MainWindow  # Generado por PyQt Designer
import consultas
import sqlite3
from datetime import date


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Inicializar métodos
        self.inicializar_ui()
        
        

    def inicializar_ui(self):
        self.consultitas=consultas.consultas_db()
        
        """Configura los eventos iniciales y carga las tablas y comboboxes."""
        self.cargar_tabla_cliente()
        self.cargar_tabla_producto()
        self.configurar_tabla_factura()
        self.cargar_tabla_reportes()
        self.cargar_tabla_localidades()
        self.cargar_tabla_provincias()
        self.cargar_tabla_documentos()

        # Conexión de botones
        self.ui.pushCliente.clicked.connect(self.grabar_datos_cliente)
        self.ui.pushEditarCliente.clicked.connect(self.modificar_datos_cliente)
        self.ui.pushAgregarStock.clicked.connect(self.grabar_datos_producto)
        self.ui.pushEditarStock.clicked.connect(self.modificar_datos_producto)
        self.ui.pushFacturar.clicked.connect(self.facturar)
        self.ui.pushBorrarCliente.clicked.connect(self.borrar_datos_cliente)
        self.ui.pushEliminarStock.clicked.connect(self.borrar_datos_producto)
        self.ui.pushAgregaLoc.clicked.connect(self.grabar_datos_localidad)
        self.ui.pushEditaLocal.clicked.connect(self.modificar_datos_localidad)
        self.ui.pushBorraLocalidad.clicked.connect(self.borrar_datos_localidad)
        self.ui.pushAgregaProv.clicked.connect(self.grabar_datos_provincia)
        self.ui.pushEditaProv.clicked.connect(self.modificar_datos_provincia)
        self.ui.pushBorraProv.clicked.connect(self.borrar_datos_provincia)
        self.ui.pushAgregaDoc.clicked.connect(self.grabar_datos_documento)
        self.ui.pushEditaDoc.clicked.connect(self.modificar_datos_documento)
        self.ui.pushBorraDoc.clicked.connect(self.borrar_datos_documento)
        fecha_hoy = date.today()
        
        self.ui.dateEdit.setDate(fecha_hoy)
        
    def configurar_tabla_factura(self):
        """Configura la tabla de factura en la pestaña correspondiente."""
        self.modelo_factura = QStandardItemModel()
        self.modelo_factura.setHorizontalHeaderLabels(["Cod. Artículo", "Descripción", "Precio", "Cantidad", "Subtotal"])
        self.ui.tablaFactura.setModel(self.modelo_factura)

        # Configurar eventos adicionales
        self.cargar_cmb_cliente()
        self.cargar_cmb_articulo()
        self.ui.spCantFac.setMaximum(self.calcular_maximo_stock())
        self.ui.pushAgregaItem.clicked.connect(self.agregar_item_factura)
        self.ui.pushBorrarItem.clicked.connect(self.borrar_item_factura)
        self.ui.cmbArticulo.currentIndexChanged.connect(self.on_combobox_articulo_changed)

    def on_combobox_articulo_changed(self):
        self.ui.spCantFac.setMaximum(self.calcular_maximo_stock())

    def cargar_cmb_cliente(self):
        """Carga el combobox de clientes con datos de la base de datos."""
        self.ui.cmbCliente.clear()
        clientes = self.consultitas.obtener_clientes()
       

        for clave, valor in clientes.items():
            self.ui.cmbCliente.addItem(valor, clave)  # Usar addItem(texto, userData)
            

    def cargar_cmb_articulo(self):
        """Carga el combobox de artículos con datos de la base de datos."""
        self.ui.cmbArticulo.clear()
        articulos = self.consultitas.obtener_articulos()

        for clave, valor in articulos.items():
            self.ui.cmbArticulo.addItem(valor, clave)  # Usar addItem(texto, userData)

    def cargar_cmb_tipo(self):
        """Carga el combobox de tipos de documento."""
        self.ui.cmbTipo.clear()
        tipos = self.consultitas.obtener_tipos()

        for clave, valor in tipos.items():
            self.ui.cmbTipo.addItem(valor, clave)  # Usar addItem(texto, userData)

    def cargar_cmb_localidad(self):
        """Carga el combobox de localidades."""
        self.ui.cmbLocalidad.clear()
        localidades = self.consultitas.obtener_localidad()

        for clave, valor in localidades.items():
            self.ui.cmbLocalidad.addItem(valor, clave)  # Usar addItem(texto, userData)
    
    def cargar_cmb_provinicia(self):
        """Carga el combobox de clientes con datos de la base de datos."""
        self.ui.cmbProvinica.clear()
        provincias = self.consultitas.obtener_provincias()
        

        for clave, valor in provincias.items():
            self.ui.cmbProvinica.addItem(valor, clave)  # Usar addItem(texto, userData)            
            
    def cargar_tabla_reportes(self):
        """Carga la tabla de clientes con datos de la base de datos."""
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(
            [ "Cod Factura","Fecha", "Nombre", "Tipo Doc.", "Nro. Doc.", "Total"])
        datos_facturas = self.consultitas.buscar_facturas("%")

        for factura in datos_facturas:
            fila = [QStandardItem(str(dato)) for dato in factura]
            modelo.appendRow(fila)

        self.ui.tablaReportes.setModel(modelo)
        self.ui.tablaReportes.selectionModel().selectionChanged.connect(self.procesar_seleccion_factura)
       
        
    def cargar_tabla_cliente(self):
        """Carga la tabla de clientes con datos de la base de datos."""
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(
            ["Cod. Cliente", "Nombre", "Cod. Doc", "Tipo Doc.", "Nro. Doc.", "Domicilio", "Id Loc", "Localidad",
             "Provincia"])
        datos_clientes = self.consultitas.buscar_clientes("%")
        

        for cliente in datos_clientes:
            fila = [QStandardItem(str(dato)) for dato in cliente]
            modelo.appendRow(fila)

        self.ui.tabla_clientes.setModel(modelo)
        self.ui.tabla_clientes.selectionModel().selectionChanged.connect(self.procesar_seleccion_cliente)
        self.cargar_cmb_tipo()
        self.cargar_cmb_localidad()
        self.cargar_cmb_cliente()

    def cargar_tabla_producto(self):
        """Carga la tabla de productos con datos de la base de datos."""
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(["Cod. Producto", "Descripción", "Precio Venta", "Stock"])
        datos_productos = self.consultitas.buscar_productos("%")

        for producto in datos_productos:
            fila = [QStandardItem(str(dato)) for dato in producto]
            modelo.appendRow(fila)

        self.ui.tablaStock.setModel(modelo)
        self.ui.tablaStock.selectionModel().selectionChanged.connect(self.procesar_seleccion_producto)

    def cargar_tabla_localidades(self):
        """Carga la tabla de localidades con datos de la base de datos."""
        self.cargar_cmb_provinicia()
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(
            [ "Cod Localidad","Nombre", "Cod Provincia", "Id Provincia"])
        datos_localidad= self.consultitas.buscar_localidad("%")

        for localidad in datos_localidad:
            fila = [QStandardItem(str(dato)) for dato in localidad]
            modelo.appendRow(fila)

        self.ui.tablaLocalidades.setModel(modelo)
        self.ui.tablaLocalidades.selectionModel().selectionChanged.connect(self.procesar_seleccion_localidad)
    
    def cargar_tabla_documentos(self):
        """Carga la tabla de documentos con datos de la base de datos."""
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(
            [ "Cod Documento","Nombre"])
        datos_documento= self.consultitas.buscar_documento("%")

        for documento in datos_documento:
            fila = [QStandardItem(str(dato)) for dato in documento]
            modelo.appendRow(fila)

        self.ui.tablaDocumentos.setModel(modelo)
        self.ui.tablaDocumentos.selectionModel().selectionChanged.connect(self.procesar_seleccion_documento)        
    
    def cargar_tabla_provincias(self):
        """Carga la tabla de localidades con datos de la base de datos."""
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(
            [ "Cod Provincia","Nombre"])
        datos_provincia= self.consultitas.buscar_provincia("%")

        for provincia in datos_provincia:
            fila = [QStandardItem(str(dato)) for dato in provincia]
            modelo.appendRow(fila)

        self.ui.tablaProvincias.setModel(modelo)
        self.ui.tablaProvincias.selectionModel().selectionChanged.connect(self.procesar_seleccion_provincia)        
        
        

    def borrar_item_factura(self):
        """Borra un item de la tabla de factura."""
        selected = self.ui.tablaFactura.selectionModel().selectedRows()
        if selected:
            index = selected[0]
            self.modelo_factura.removeRow(index.row())
            self.ui.txtTotal.setText(str(self.calcular_total_factura()))

    def agregar_item_factura(self):
        """Agrega un nuevo artículo a la tabla de factura."""
        articulo_id = self.ui.cmbArticulo.currentData()  # Obtener el ID del artículo
        if self.existe_item_factura(articulo_id):
            QMessageBox.information(self, "Información", "El artículo ya está cargado en la tabla")
            return

        descripcion = self.ui.cmbArticulo.currentText()
        precio = self.consultitas.obtener_precio(articulo_id)
        cantidad = self.ui.spCantFac.value()
        subtotal = precio * cantidad

        fila = [
            QStandardItem(str(articulo_id)),
            QStandardItem(descripcion),
            QStandardItem(str(precio)),
            QStandardItem(str(cantidad)),
            QStandardItem(str(subtotal))
        ]

        self.modelo_factura.appendRow(fila)
        self.ui.txtTotal.setText(str(self.calcular_total_factura()))

    def grabar_datos_cliente(self):
        """Graba los datos de cliente en la base de datos."""
        nombre = self.ui.txtNombre.text()
        domicilio = self.ui.txtDomicilio.text()
        id_documento = self.ui.cmbTipo.currentData()  # Obtener el ID del tipo de documento
        documento = self.ui.txtDocumento.text()
        id_localidad = self.ui.cmbLocalidad.currentData()  # Obtener el ID de la localidad

        try:
            self.consultitas.grabar_clientes(nombre, domicilio, id_documento, documento, id_localidad)
            self.cargar_tabla_cliente()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al grabar los datos: {e}")

    def modificar_datos_cliente(self):
        """Modifica los datos de cliente en la base de datos."""
        codigo = self.ui.txtCodigo.text()
        nombre = self.ui.txtNombre.text()
        domicilio = self.ui.txtDomicilio.text()
        id_documento = self.ui.cmbTipo.currentData()  # Obtener el ID del tipo de documento
        documento = self.ui.txtDocumento.text()
        id_localidad = self.ui.cmbLocalidad.currentData()  # Obtener el ID de la localidad

        try:
            self.consultitas.modificar_cliente(codigo, nombre, domicilio, id_documento, documento, id_localidad)
            self.cargar_tabla_cliente()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al modificar los datos: {e}")
    def borrar_datos_cliente(self):
        """Modifica los datos de cliente en la base de datos."""
        codigo = self.ui.txtCodigo.text()
        
        try:
            self.consultitas.borrar_cliente(codigo)
            self.cargar_tabla_cliente()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al modificar los datos: {e}")            
            
    def grabar_datos_localidad(self):
        """Graba los datos de localidad en la base de datos."""
        nombre = self.ui.txtNombreLoc.text()
        id_provincia = self.ui.cmbProvinica.currentData()  # Obtener el ID de la localidad

        try:
            self.consultitas.grabar_localidad(nombre, id_provincia)
            self.cargar_cmb_localidad()
            self.cargar_tabla_localidades()
            QMessageBox.information(self, "Info", "Localidad grabada con exito")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al grabar los datos: {e}")
    
    def modificar_datos_localidad(self):
        """Modifica los datos de cliente en la base de datos."""
        codigo = self.ui.txtCodLoc.text()
        nombre = self.ui.txtNombreLoc.text()
        id_provincia = self.ui.cmbProvinica.currentData()  # Obtener el ID de la localidad
        

        try:
            self.consultitas.modificar_localidad(codigo, nombre, id_provincia)
            self.cargar_tabla_localidades()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al modificar los datos: {e}")            
    
    def borrar_datos_localidad(self):
        """Modifica los datos de cliente en la base de datos."""
        codigo = self.ui.txtCodLoc.text()
        
        try:
            self.consultitas.borrar_localidad(codigo)
            self.cargar_tabla_localidades()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al borrar los datos: {e}")            
            
    def grabar_datos_provincia(self):
        """Graba los datos de localidad en la base de datos."""
        nombre = self.ui.txtNombProv.text()
        try:
            self.consultitas.grabar_provincia(nombre)
            self.cargar_tabla_provincias()
            self.cargar_cmb_provinicia()
            QMessageBox.information(self, "Info", "Provincia grabada con exito")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al grabar los datos: {e}")
    
    def modificar_datos_provincia(self):
        """Modifica los datos de cliente en la base de datos."""
        codigo = self.ui.txtCodProv.text()
        nombre = self.ui.txtNombProv.text()
               

        try:
            self.consultitas.modificar_provincia(codigo, nombre)
            self.cargar_tabla_provincias()
            self.cargar_cmb_provinicia()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al modificar los datos: {e}")            
    
    def borrar_datos_provincia(self):
        """Modifica los datos de cliente en la base de datos."""
        codigo = self.ui.txtCodProv.text()
        
        try:
            self.consultitas.borrar_provincia(codigo)
            self.cargar_cmb_provinicia()
            self.cargar_tabla_provincias()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al borrar los datos: {e}")            
            
    def grabar_datos_documento(self):
        """Graba los datos de localidad en la base de datos."""
        nombre = self.ui.txtNomDoc.text()
        try:
            self.consultitas.grabar_documento(nombre)
            self.cargar_tabla_documentos()
            self.cargar_cmb_tipo()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al grabar los datos: {e}")
    
    def modificar_datos_documento(self):
        """Modifica los datos de cliente en la base de datos."""
        codigo = self.ui.txtCodDoc.text()
        nombre = self.ui.txtNomDoc.text()
               

        try:
            self.consultitas.modificar_documento(codigo, nombre)
            self.cargar_tabla_documentos()
            self.cargar_cmb_tipo()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al modificar los datos: {e}")            
    
    def borrar_datos_documento(self):
        """Modifica los datos de documento en la base de datos."""
        codigo = self.ui.txtCodDoc.text()
        
        try:
            self.consultitas.borrar_documento(codigo)
            self.cargar_tabla_documentos()
            self.cargar_cmb_tipo()
            
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al borrar los datos: {e}")                        
            
    def procesar_seleccion_cliente(self, selected, deselected):
        """Procesa la selección de filas en la tabla de clientes."""
        if selected.indexes():
            index = selected.indexes()[0]
            fila = index.row()
            self.mostrar_datos_cliente(fila)

    def procesar_seleccion_producto(self, selected, deselected):
        """Procesa la selección de filas en la tabla de productos."""
        if selected.indexes():
            index = selected.indexes()[0]
            fila = index.row()
            self.mostrar_datos_producto(fila)
            
    def procesar_seleccion_factura(self, selected, deselected):
        """Procesa la selección de filas en la tabla de clientes."""
        if selected.indexes():
            index = selected.indexes()[0]
            fila = index.row()
            #self.mostrar_datos_cliente(fila)       
    def procesar_seleccion_factura(self, selected, deselected):
        """Procesa la selección de filas en la tabla de reportes."""
        if selected.indexes():
            index = selected.indexes()[0]
            fila = index.row()
            modelo = self.ui.tablaReportes.model()
            cod_factura = modelo.data(modelo.index(fila, 0))
            self.mostrar_detalle_factura(cod_factura)
    
    def procesar_seleccion_localidad(self, selected, deselected):
        """Procesa la selección de filas en la tabla de localidad"""
        if selected.indexes():
            index = selected.indexes()[0]
            fila = index.row()
            self.mostrar_datos_localidad(fila)
    
    def procesar_seleccion_provincia(self, selected, deselected):
        """Procesa la selección de filas en la tabla de localidad"""
        if selected.indexes():
            index = selected.indexes()[0]
            fila = index.row()
            self.mostrar_datos_provincia(fila)
    
    def procesar_seleccion_documento(self, selected, deselected):
        """Procesa la selección de filas en la tabla de documentos"""
        if selected.indexes():
            index = selected.indexes()[0]
            fila = index.row()
            self.mostrar_datos_documento(fila)
             
     
        
    
    def mostrar_detalle_factura(self, cod_factura):
            """Muestra una ventana con el detalle de la factura."""
            dialogo = DetalleFacturaDialog(cod_factura)
            dialogo.exec_()
            

    def mostrar_datos_cliente(self, fila):
        """Muestra los datos del cliente seleccionado en los campos de la interfaz."""
        modelo = self.ui.tabla_clientes.model()
        cod_cliente = modelo.data(modelo.index(fila, 0))
        nombre = modelo.data(modelo.index(fila, 1))
        tipo = modelo.data(modelo.index(fila, 2))
        localidad = modelo.data(modelo.index(fila, 6))
        domicilio = modelo.data(modelo.index(fila, 5))
        documento = modelo.data(modelo.index(fila, 4))

        self.ui.txtCodigo.setText(cod_cliente)
        self.ui.txtNombre.setText(nombre)
        self.ui.cmbTipo.setCurrentIndex(self.ui.cmbTipo.findData(tipo))
        self.ui.cmbLocalidad.setCurrentIndex(self.ui.cmbLocalidad.findData(localidad))
        self.ui.txtDomicilio.setText(domicilio)
        self.ui.txtDocumento.setValue(float(documento))

    def mostrar_datos_producto(self, fila):
        """Muestra los datos del producto seleccionado en los campos de la interfaz."""
        modelo = self.ui.tablaStock.model()
        cod_producto = modelo.data(modelo.index(fila, 0))
        descripcion = modelo.data(modelo.index(fila, 1))
        precio_venta = modelo.data(modelo.index(fila, 2))
        stock = modelo.data(modelo.index(fila, 3))

        self.ui.txtProducto.setText(cod_producto)
        self.ui.txtDescripcion.setText(descripcion)
        self.ui.SpPrecio.setValue(float(precio_venta))
        self.ui.spStock.setValue(int(stock))
    
    def mostrar_datos_localidad(self, fila):
        """Muestra los datos del cliente seleccionado en los campos de la interfaz."""
        modelo = self.ui.tablaLocalidades.model()
        cod_localidad = modelo.data(modelo.index(fila, 0))
        nombre = modelo.data(modelo.index(fila, 1))
        cod_provincia = modelo.data(modelo.index(fila, 2))
        
        self.ui.txtCodLoc.setText(cod_localidad)
        self.ui.txtNombreLoc.setText(nombre)
        self.ui.cmbProvinica.setCurrentIndex(self.ui.cmbProvinica.findData(cod_provincia))
        
    def mostrar_datos_provincia(self, fila):
        """Muestra los datos del cliente seleccionado en los campos de la interfaz."""
        modelo = self.ui.tablaProvincias.model()
        cod_provincia = modelo.data(modelo.index(fila, 0))
        nombre = modelo.data(modelo.index(fila, 1))
        
        self.ui.txtCodProv.setText(cod_provincia)
        self.ui.txtNombProv.setText(nombre)
        
    def mostrar_datos_documento(self, fila):
        """Muestra los datos del cliente seleccionado en los campos de la interfaz."""
        modelo = self.ui.tablaDocumentos.model()
        cod_documento = modelo.data(modelo.index(fila, 0))
        nombre = modelo.data(modelo.index(fila, 1))
        
        self.ui.txtCodDoc.setText(cod_documento)
        self.ui.txtNomDoc.setText(nombre)        
        
        

    def grabar_datos_producto(self):
        """Graba los datos de producto en la base de datos."""
        descripcion = self.ui.txtDescripcion.text()
        stock = self.ui.spStock.value()
        precio = self.ui.SpPrecio.value()

        try:
            self.consultitas.grabar_stock(descripcion, stock, precio)
            self.cargar_tabla_producto()
            self.cargar_cmb_articulo()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al grabar los datos: {e}")

    def modificar_datos_producto(self):
        """Modifica los datos de producto en la base de datos."""
        codigo = self.ui.txtProducto.text()
        descripcion = self.ui.txtDescripcion.text()
        stock = self.ui.spStock.value()
        precio = self.ui.SpPrecio.value()

        try:
            self.consultitas.modificar_stock(descripcion, stock, precio, codigo)
            self.cargar_tabla_producto()
            self.cargar_cmb_articulo()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al modificar los datos: {e}")
            

    def existe_item_factura(self, codigo):
        """Verifica si un artículo ya existe en la tabla de factura."""
        modelo = self.ui.tablaFactura.model()
        if modelo is None:
            return False

        for fila in range(modelo.rowCount()):
            indice = modelo.data(modelo.index(fila, 0))
            if str(indice) == str(codigo):
                return True
        return False

    def calcular_total_factura(self):
        """Calcula el total de la factura."""
        total = 0
        modelo = self.ui.tablaFactura.model()
        if modelo is None:
            return total

        for fila in range(modelo.rowCount()):
            indice = float(modelo.data(modelo.index(fila, 4)))
            total += indice
        return total

    def facturar(self):
        """Graba la factura y los items de la factura en la base de datos."""
        modelo = self.ui.tablaFactura.model()
        if modelo is None or modelo.rowCount() == 0:
            QMessageBox.information(self, "Información", "La tabla de factura está vacía")
            return

        fecha = self.ui.dateEdit.text()
        cliente = self.ui.cmbCliente.currentData()  # Obtener el ID del cliente
        total = self.ui.txtTotal.text()

        try:
            numero_factura = self.consultitas.grabar_factura(fecha, cliente, total)
        

            for fila in range(modelo.rowCount()):
                codigo = int(modelo.data(modelo.index(fila, 0)))
                cantidad = float(modelo.data(modelo.index(fila, 3)))
                precio = float(modelo.data(modelo.index(fila, 2)))
                self.consultitas.grabar_item_factura(numero_factura, codigo, cantidad, precio)
                self.consultitas.actualizar_stock(codigo, cantidad)
                

            QMessageBox.information(self, "Información", f"Factura {numero_factura} grabada con éxito")
            self.cargar_tabla_producto()
            self.cargar_tabla_reportes()
            # Limpiar la tabla de factura después de grabar
            self.modelo_factura.clear()
            self.ui.txtTotal.setText("0")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al grabar la factura: {e}")
            
    def borrar_datos_producto(self):
        """Borrra los datos de stock en la base de datos."""
        codigo = self.ui.txtProducto.text()
        
        try:
            self.consultitas.borrar_producto(codigo)
            self.cargar_tabla_producto()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al modificar los datos: {e}")            
            

    def calcular_maximo_stock(self):
        """Calcula el máximo stock disponible para el artículo seleccionado."""
        if self.ui.cmbArticulo.currentIndex() is None:
            return 0
        maximo = self.consultitas.buscar_maximo(self.ui.cmbArticulo.currentData())
        return maximo

class DetalleFacturaDialog(QDialog):
    def __init__(self, cod_factura):
        super().__init__()
        self.setWindowTitle(f"Detalle de Factura {cod_factura}")
        self.cod_factura = cod_factura
        self.initUI()
        

    def initUI(self):
        self.consultitas=consultas.consultas_db()
        layout = QVBoxLayout()

        # Obtener datos de la factura
        datos_factura = self.consultitas.obtener_datos_factura(self.cod_factura)
        if datos_factura:
            fecha, cliente_nombre, total = datos_factura
            #cliente_nombre = self.consultitas.obtener_nombre_cliente(cliente_id)

            # Mostrar datos de la cabecera de la factura
            layout.addWidget(QLabel(f"Factura Nro: {self.cod_factura}"))
            layout.addWidget(QLabel(f"Fecha: {fecha}"))
            layout.addWidget(QLabel(f"Cliente: {cliente_nombre}"))

            # Crear tabla para los items de la factura
            tabla_items = QTableView()
            modelo_items = QStandardItemModel()
            modelo_items.setHorizontalHeaderLabels(["Descripción", "Cantidad", "Precio", "Subtotal"])

            # Obtener items de la factura
            items_factura = self.consultitas.obtener_items_factura(self.cod_factura)
            for item in items_factura:
                descripcion, cantidad, precio, subtotal = item
                fila = [
                    QStandardItem(descripcion),
                    QStandardItem(str(cantidad)),
                    QStandardItem(str(precio)),
                    QStandardItem(str(subtotal))
                ]
                modelo_items.appendRow(fila)

            tabla_items.setModel(modelo_items)
            layout.addWidget(tabla_items)

            # Mostrar total de la factura
            layout.addWidget(QLabel(f"Total: {total}"))

        else:
            layout.addWidget(QLabel(f"No se encontró la factura {self.cod_factura}"))

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())