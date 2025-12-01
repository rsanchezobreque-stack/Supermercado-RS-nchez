import csv

def producto_mas_caro(path):
    with open(path, "r", newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        max_precio = -1
        producto_caro = None
        for fila in lector:
            if len(fila) < 3:
                continue
            nombre = fila[1]
            try:
                precio = float(fila[2])
            except:
                precio = 0.0
            if precio > max_precio:
                max_precio = precio
                producto_caro = nombre
        return producto_caro, max_precio

archivo = "productos.csv"
nombre, precio = producto_mas_caro(archivo)
print(f"\nEl producto más caro es: {nombre}")
print(f"Con un precio de: {precio}")



import csv

def valorTotalBodega(path):
    total = 0
    with open(path, "r", newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        for fila in lector:
            if len(fila) < 4:
                continue
            try:
                precio = float(fila[2])
                cantidad = float(fila[3])
            except:
                precio, cantidad = 0.0, 0.0
            total += precio * cantidad
    return total

archivo = "productos.csv"
print(f"La bodega vale en total {valorTotalBodega(archivo)}")



import csv

ITEMS_PATH = "items.csv"
PRODUCTOS_PATH = "productos.csv"

# Leer productos
info_productos = {}
with open(PRODUCTOS_PATH, "r", newline="", encoding="utf-8") as f:
    lector = csv.reader(f)
    for fila in lector:
        if len(fila) < 3:
            continue
        id_prod = fila[0]
        nombre = fila[1]
        try:
            precio = float(fila[2])
        except:
            t = fila[2].replace(".", "").replace(",", ".")
            try:
                precio = float(t)
            except:
                precio = 0.0
        info_productos[id_prod] = (nombre, precio)

# Calcular ingresos
ingresos = {}
with open(ITEMS_PATH, "r", newline="", encoding="utf-8") as f:
    lector = csv.reader(f)
    for fila in lector:
        if len(fila) < 3:
            continue
        id_prod = fila[1]
        try:
            cantidad = float(fila[2])
        except:
            t = fila[2].replace(".", "").replace(",", ".")
            try:
                cantidad = float(t)
            except:
                cantidad = 0.0
        if id_prod in info_productos:
            nombre, precio = info_productos[id_prod]
            ingresos[nombre] = ingresos.get(nombre, 0) + precio * cantidad

# Mostrar resultados
if not ingresos:
    print("No se pudieron calcular ingresos. Revisa los archivos.")
else:
    orden = sorted(ingresos.items(), key=lambda x: x[1], reverse=True)
    print("Ingresos por producto (descendente):")
    for nombre, ingreso in orden:
        ingreso_str = f"{int(ingreso)}" if abs(ingreso - int(ingreso)) < 1e-9 else f"{ingreso:.2f}"
        print(f" - {nombre}: {ingreso_str}")

    producto_mayor, mayor_valor = orden[0]
    mayor_str = f"{int(mayor_valor)}" if abs(mayor_valor - int(mayor_valor)) < 1e-9 else f"{mayor_valor:.2f}"
    print("\nProducto con más ingresos:")
    print(f"{producto_mayor}  →  {mayor_str}")



import csv

def separar(linea):
    # Divide la línea por ';' y elimina espacios
    return linea.strip().split(";")

def totalVentasMes(archivo_items, archivo_productos, archivo_ventas, mes, año):
    # --- Cargar productos ---
    productos = {}
    try:
        with open(archivo_productos, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)  # saltar cabecera
            for fila in reader:
                if len(fila) >= 3:
                    idProducto, _, precio = fila[:3]
                    try:
                        productos[idProducto.strip()] = float(precio.strip())
                    except ValueError:
                        productos[idProducto.strip()] = 0.0
    except FileNotFoundError:
        print("Archivo de productos no encontrado.")
        return 0
    except Exception as e:
        print(f"Error al cargar productos: {e}")
        return 0

    # --- Cargar ítems ---
    items_por_venta = {}
    try:
        with open(archivo_items, "r", encoding="utf-8") as f:
            next(f)  # saltar cabecera
            for linea in f:
                partes = separar(linea)
                if len(partes) >= 3:
                    idVenta, idProducto, cantidad = partes[:3]
                    if idVenta not in items_por_venta:
                        items_por_venta[idVenta] = []
                    try:
                        cantidad = int(cantidad)
                    except ValueError:
                        cantidad = 0
                    items_por_venta[idVenta].append((idProducto, cantidad))
    except FileNotFoundError:
        print("Archivo de ítems no encontrado.")
        return 0
    except Exception as e:
        print(f"Error al cargar ítems: {e}")
        return 0

    # --- Calcular ventas ---
    total = 0
    try:
        with open(archivo_ventas, "r", encoding="utf-8") as f:
            next(f)  # saltar cabecera
            for linea in f:
                partes = separar(linea)
                if len(partes) >= 2:
                    idVenta, fecha = partes[:2]
                    try:
                        dia, mesVenta, añoVenta = fecha.split("-")
                    except ValueError:
                        continue

                    if int(mesVenta) == mes and int(añoVenta) == año:
                        if idVenta in items_por_venta:
                            for idProducto, cantidad in items_por_venta[idVenta]:
                                if idProducto in productos:
                                    precio = productos[idProducto]
                                    total += precio * cantidad
    except FileNotFoundError:
        print("Archivo de ventas no encontrado.")
        return 0
    except Exception as e:
        print(f"Error al calcular ventas: {e}")
        return 0

    return total

# --- Parámetros de consulta ---
MES_CONSULTA = 9
AÑO_CONSULTA = 2010

resultado = totalVentasMes(
    archivo_items="items.csv",
    archivo_productos="productos.csv",
    archivo_ventas="ventas.csv",
    mes=MES_CONSULTA,
    año=AÑO_CONSULTA
)

print(f"El total de ventas para el mes {MES_CONSULTA:02d} del año {AÑO_CONSULTA} es: ${resultado:,.2f}")

