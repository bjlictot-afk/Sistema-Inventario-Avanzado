# servicios/inventario.py
import json
import os
from modelos.producto import Producto

class Inventario:
    """Clase que maneja el inventario de productos de la tienda."""

    def __init__(self, archivo=None):
        self.productos = {}  # Diccionario {id: Producto}
        if archivo is None:
            # Definir la ruta absoluta al archivo dentro de la carpeta datos
            archivo = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos", "inventario.txt")
        self.archivo = archivo
        self.cargar_archivo()

    # Añadir producto
    def añadir_producto(self, producto):
        if producto.get_id() in self.productos:
            print("❌ Error: El ID ya existe.")
        else:
            self.productos[producto.get_id()] = producto
            self.guardar_archivo()
            print("✅ Producto añadido correctamente.")

    # Eliminar producto por ID
    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_archivo()
            print("✅ Producto eliminado.")
        else:
            print("❌ Producto no encontrado.")

    # Actualizar cantidad y/o precio de un producto
    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].set_cantidad(cantidad)
            if precio is not None:
                self.productos[id_producto].set_precio(precio)
            self.guardar_archivo()
            print("✅ Producto actualizado.")
        else:
            print("❌ Producto no encontrado.")

    # Buscar productos por nombre (puede devolver varios resultados)
    def buscar_por_nombre(self, nombre):
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print("❌ No se encontraron productos.")

    # Mostrar todos los productos
    def mostrar_todos(self):
        if not self.productos:
            print("Inventario vacío.")
        else:
            for p in self.productos.values():
                print(p)

    # Guardar inventario en archivo JSON
    def guardar_archivo(self):
        with open(self.archivo, "w") as f:
            datos = [p.to_dict() for p in self.productos.values()]
            json.dump(datos, f, indent=4)

    # Cargar inventario desde archivo JSON
    def cargar_archivo(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                try:
                    datos = json.load(f)
                    for item in datos:
                        producto = Producto(
                            item["id"],
                            item["nombre"],
                            item["cantidad"],
                            item["precio"]
                        )
                        self.productos[item["id"]] = producto
                except json.JSONDecodeError:
                    print("⚠️ Archivo vacío o corrupto.")
        else:
            print("Archivo no encontrado. Se creará uno nuevo.")

    # Mostrar resumen del inventario
    def resumen(self):
        total_items = sum(p.get_cantidad() for p in self.productos.values())
        valor_total = sum(p.get_cantidad() * p.get_precio() for p in self.productos.values())
        print("\nResumen del Inventario:")
        print(f"Total de productos distintos: {len(self.productos)}")
        print(f"Cantidad total de ítems: {total_items}")
        print(f"Valor total del inventario: ${valor_total:.2f}")