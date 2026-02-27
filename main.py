import json
import os


# ==============================
# CLASE PRODUCTO
# ==============================

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Métodos getters
    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    # Métodos setters
    def set_cantidad(self, nueva_cantidad):
        self.__cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio):
        self.__precio = nuevo_precio

    # Convertir objeto a diccionario (para guardar en archivo)
    def to_dict(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio
        }


# ==============================
# CLASE INVENTARIO
# ==============================

class Inventario:
    def __init__(self, archivo="inventario.txt"):
        self.productos = {}  # Diccionario: {id: Producto}
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

    # Eliminar producto
    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_archivo()
            print("✅ Producto eliminado.")
        else:
            print("❌ Producto no encontrado.")

    # Actualizar producto
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

    # Buscar por nombre
    def buscar_por_nombre(self, nombre):
        encontrados = [
            p for p in self.productos.values()
            if nombre.lower() in p.get_nombre().lower()
        ]

        if encontrados:
            for p in encontrados:
                print(f"ID: {p.get_id()} | Nombre: {p.get_nombre()} | "
                      f"Cantidad: {p.get_cantidad()} | Precio: ${p.get_precio()}")
        else:
            print("❌ No se encontraron productos.")

    # Mostrar todos
    def mostrar_todos(self):
        if not self.productos:
            print("Inventario vacío.")
        else:
            for p in self.productos.values():
                print(f"ID: {p.get_id()} | Nombre: {p.get_nombre()} | "
                      f"Cantidad: {p.get_cantidad()} | Precio: ${p.get_precio()}")

    # Guardar en archivo (serialización)
    def guardar_archivo(self):
        with open(self.archivo, "w") as f:
            datos = [p.to_dict() for p in self.productos.values()]
            json.dump(datos, f, indent=4)

    # Cargar desde archivo (deserialización)
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
                except:
                    print("Archivo vacío o corrupto.")
        else:
            print("Archivo no encontrado. Se creará uno nuevo.")


# ==============================
# MENÚ INTERACTIVO
# ==============================

def menu():
    inventario = Inventario()

    while True:
        print("\n===== SISTEMA AVANZADO DE INVENTARIO =====")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = input("ID: ")
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))

            producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.añadir_producto(producto)

        elif opcion == "2":
            id_producto = input("Ingrese ID a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = input("Ingrese ID a actualizar: ")
            cantidad = input("Nueva cantidad (Enter para omitir): ")
            precio = input("Nuevo precio (Enter para omitir): ")

            cantidad = int(cantidad) if cantidad else None
            precio = float(precio) if precio else None

            inventario.actualizar_producto(id_producto, cantidad, precio)

        elif opcion == "4":
            nombre = input("Ingrese nombre a buscar: ")
            inventario.buscar_por_nombre(nombre)

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
