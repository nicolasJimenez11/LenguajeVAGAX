def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        raise Exception(f"No se encontró el archivo: {ruta}")
    except Exception as e:
        raise Exception(f"Error al leer el archivo '{ruta}': {e}")


def escribir_archivo(nombre, contenido):
    try:
        with open(nombre, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        return True
    except Exception as e:
        raise Exception(f"Error al escribir el archivo '{nombre}': {e}")