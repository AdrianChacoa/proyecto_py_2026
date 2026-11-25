
import sqlite3


DB_NAME = "productos.db"


def crear_tabla():

    conexion = sqlite3.connect(DB_NAME)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos preparada correctamente.")



def agregar_producto():

    print("\n--- AGREGAR PRODUCTO ---")

    nombre = input("Ingrese el nombre: ").strip()

    if nombre == "":
        print("El nombre no puede estar vacio.")
        return

    
    while True:
        try:
            precio = float(
                input("Ingrese el precio: ").replace(",", ".")
            )

            if precio < 0:
                print("El precio no puede ser negativo.")
                continue

            break

        except ValueError:
            print("Ingrese un precio numerico valido.")

    while True:
        try:
            stock = int(input("Ingrese el stock: "))

            if stock < 0:
                print("El stock no puede ser negativo.")
                continue

            break

        except ValueError:
            print("Ingrese una cantidad entera valida.")

    conexion = sqlite3.connect(DB_NAME)

    conexion.execute(
        """
        INSERT INTO productos (nombre, precio, stock)
        VALUES (?, ?, ?)
        """,
        (nombre, precio, stock)
    )

    conexion.commit()
    conexion.close()

    print("Producto agregado correctamente.")


# ==========================================
# 3. LISTAR PRODUCTOS
# ==========================================

def listar_productos():

    conexion = sqlite3.connect(DB_NAME)

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos ORDER BY id")

    productos = cursor.fetchall()

    conexion.close()

    print("\n--- LISTA DE PRODUCTOS ---")

    if len(productos) == 0:
        print("No hay productos registrados.")
        return

    for producto in productos:

        print("-------------------------")
        print("ID:", producto[0])
        print("Nombre:", producto[1])
        print("Precio: $", producto[2])
        print("Stock:", producto[3])


# ==========================================
# 4. BUSCAR PRODUCTOS
# ==========================================

def buscar_producto():

    nombre = input("\nIngrese el nombre a buscar: ").strip()

    if nombre == "":
        print("Debe ingresar un nombre.")
        return

    conexion = sqlite3.connect(DB_NAME)

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM productos WHERE nombre LIKE ? COLLATE NOCASE",
        ("%" + nombre + "%",)
    )

    resultados = cursor.fetchall()

    conexion.close()

    if resultados:

        print("\n--- PRODUCTOS ENCONTRADOS ---")

        for producto in resultados:

            print("-------------------------")
            print("ID:", producto[0])
            print("Nombre:", producto[1])
            print("Precio: $", producto[2])
            print("Stock:", producto[3])

    else:
        print("No se encontraron productos.")


# ==========================================
# 5. ELIMINAR PRODUCTOS
# ==========================================

def eliminar_producto():

    listar_productos()

    try:
        id_producto = int(
            input("\nIngrese el ID del producto a eliminar: ")
        )

        conexion = sqlite3.connect(DB_NAME)

        cursor = conexion.cursor()

        cursor.execute(
            "SELECT nombre FROM productos WHERE id = ?",
            (id_producto,)
        )

        producto = cursor.fetchone()

        if producto is None:
            print("No existe un producto con ese ID.")
            conexion.close()
            return

        print("Producto seleccionado:", producto[0])

        confirmacion = input(
            "¿Esta seguro de eliminarlo? (S/N): "
        ).strip().upper()

        if confirmacion == "S":

            cursor.execute(
                "DELETE FROM productos WHERE id = ?",
                (id_producto,)
            )

            conexion.commit()

            print("Producto eliminado correctamente.")

        else:
            print("Eliminacion cancelada.")

        conexion.close()

    except ValueError:
        print("Debe ingresar un ID numerico.")



# ==========================================
# 6. MENU PRINCIPAL
# ==========================================

def menu():

    while True:

        print("\n================================")
        print("    SISTEMA DE GESTION")
        print("        DE PRODUCTOS")
        print("================================")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Buscar producto")
        print("4. Eliminar producto")
        print("5. Salir")
        print("================================")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            agregar_producto()

        elif opcion == "2":
            listar_productos()

        elif opcion == "3":
            buscar_producto()

        elif opcion == "4":
            eliminar_producto()

        elif opcion == "5":
            print("Gracias por utilizar el sistema.")
            break

        else:
            print("Opcion incorrecta.")


# ==========================================
# 7. INICIAR EL PROGRAMA
# ==========================================

if __name__ == "__main__":

    crear_tabla()

    menu()
