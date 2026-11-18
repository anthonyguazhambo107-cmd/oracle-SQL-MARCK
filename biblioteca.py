"""Sistema de consola para la biblioteca de Desarrollo de Software.

Practica de Python: listas, diccionarios, funciones, excepciones y archivos.
"""

from datetime import date


ARCHIVO_LIBROS = "libros.txt"
ARCHIVO_PRESTAMOS = "prestamos.txt"

LIBROS_INICIALES = [
    {"codigo": 1, "titulo": "Python para todos", "autor": "Charles Severance", "estado": "Disponible"},
    {"codigo": 2, "titulo": "Aprende Java", "autor": "Ana Torres", "estado": "Disponible"},
    {"codigo": 3, "titulo": "Bases de datos", "autor": "Carlos Mora", "estado": "Disponible"},
]


def guardar_libros(libros):
    """Guarda una línea por libro, con campos separados por comas."""
    with open(ARCHIVO_LIBROS, "w", encoding="utf-8") as archivo:
        for libro in libros:
            linea = f"{libro['codigo']},{libro['titulo']},{libro['autor']},{libro['estado']}\n"
            archivo.write(linea)
    return True


def cargar_libros():
    """Carga los libros desde el archivo o crea el archivo inicial."""
    libros = []
    try:
        with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                datos = linea.strip().split(",")
                if len(datos) != 4:
                    print(f"Aviso: se omitió una línea inválida en libros.txt ({numero_linea}).")
                    continue
                try:
                    libros.append({
                        "codigo": int(datos[0]),
                        "titulo": datos[1],
                        "autor": datos[2],
                        "estado": datos[3],
                    })
                except ValueError:
                    print(f"Aviso: código inválido en libros.txt ({numero_linea}).")
    except FileNotFoundError:
        print("No se encontró libros.txt: se usarán los libros iniciales.")
        libros = [dict(libro) for libro in LIBROS_INICIALES]
        guardar_libros(libros)
    return libros


def guardar_prestamos(prestamos):
    """Guarda los préstamos con número, código, estudiante, fecha y estado."""
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
        for prestamo in prestamos:
            linea = (
                f"{prestamo['numero']},{prestamo['codigo_libro']},"
                f"{prestamo['estudiante']},{prestamo['fecha']},{prestamo['estado']}\n"
            )
            archivo.write(linea)
    return True


def cargar_prestamos():
    """Carga los préstamos; si no existe el archivo, empieza con una lista vacía."""
    prestamos = []
    try:
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                datos = linea.strip().split(",")
                if len(datos) != 5:
                    print(f"Aviso: se omitió una línea inválida en prestamos.txt ({numero_linea}).")
                    continue
                try:
                    prestamos.append({
                        "numero": int(datos[0]),
                        "codigo_libro": int(datos[1]),
                        "estudiante": datos[2],
                        "fecha": datos[3],
                        "estado": datos[4],
                    })
                except ValueError:
                    print(f"Aviso: datos numéricos inválidos en prestamos.txt ({numero_linea}).")
    except FileNotFoundError:
        print("No se encontró prestamos.txt: se usará una lista vacía.")
        guardar_prestamos(prestamos)
    return prestamos


def leer_entero(mensaje):
    """Pide un número entero hasta que el usuario escriba un valor válido."""
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Error: debe escribir un número entero.")


def leer_texto(mensaje):
    """Pide texto no vacío y sin comas para mantener válido el archivo CSV simple."""
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Error: el texto no puede estar vacío.")
        elif "," in texto:
            print("Error: no se permiten comas porque separan los campos del archivo.")
        else:
            return texto


def buscar_por_codigo(libros, codigo):
    """Devuelve el libro con el código indicado o None si no existe."""
    for libro in libros:
        if libro["codigo"] == codigo:
            return libro
    return None


def registrar_libro(libros):
    """Registra un libro, asigna el siguiente código y devuelve el nuevo libro."""
    titulo = leer_texto("Título: ")
    autor = leer_texto("Autor: ")
    siguiente_codigo = max((libro["codigo"] for libro in libros), default=0) + 1
    nuevo_libro = {
        "codigo": siguiente_codigo,
        "titulo": titulo,
        "autor": autor,
        "estado": "Disponible",
    }
    libros.append(nuevo_libro)
    guardar_libros(libros)
    print(f"Libro registrado correctamente con código {siguiente_codigo}.")
    return nuevo_libro


def mostrar_libros(libros):
    """Muestra una tabla alineada y devuelve la cantidad de libros."""
    print("\n" + "=" * 78)
    print(f"{'CÓDIGO':<10}{'TÍTULO':<28}{'AUTOR':<25}{'ESTADO':<15}")
    print("-" * 78)
    if not libros:
        print("No hay libros registrados.")
    else:
        for libro in libros:
            print(
                f"{libro['codigo']:<10}{libro['titulo'][:27]:<28}"
                f"{libro['autor'][:24]:<25}{libro['estado']:<15}"
            )
    print("=" * 78)
    return len(libros)


def buscar_libro(libros):
    """Busca libros cuyo título contiene una palabra, sin distinguir mayúsculas."""
    palabra = leer_texto("Palabra a buscar en el título: ").lower()
    encontrados = [libro for libro in libros if palabra in libro["titulo"].lower()]
    if not encontrados:
        print("No se encontraron libros con esa palabra.")
    else:
        mostrar_libros(encontrados)
        print(f"Se encontraron {len(encontrados)} libro(s).")
    return len(encontrados)


def prestar_libro(libros, prestamos):
    """Presta un libro disponible y registra el préstamo activo."""
    codigo = leer_entero("Código del libro: ")
    libro = buscar_por_codigo(libros, codigo)
    if libro is None:
        print("Error: no existe un libro con ese código.")
        return False
    if libro["estado"] != "Disponible":
        print("Error: el libro no está disponible.")
        return False

    estudiante = leer_texto("Nombre del estudiante: ")
    siguiente_numero = max((prestamo["numero"] for prestamo in prestamos), default=0) + 1
    prestamos.append({
        "numero": siguiente_numero,
        "codigo_libro": codigo,
        "estudiante": estudiante,
        "fecha": str(date.today()),
        "estado": "Activo",
    })
    libro["estado"] = "Prestado"
    guardar_libros(libros)
    guardar_prestamos(prestamos)
    print(f"Préstamo registrado correctamente con número {siguiente_numero}.")
    return True


def devolver_libro(libros, prestamos):
    """Devuelve un libro prestado y marca el préstamo activo como devuelto."""
    codigo = leer_entero("Código del libro: ")
    libro = buscar_por_codigo(libros, codigo)
    if libro is None:
        print("Error: no existe un libro con ese código.")
        return False
    if libro["estado"] != "Prestado":
        print("Error: el libro no está prestado.")
        return False

    prestamo_activo = None
    for prestamo in prestamos:
        if prestamo["codigo_libro"] == codigo and prestamo["estado"] == "Activo":
            prestamo_activo = prestamo
            break
    if prestamo_activo is None:
        print("Error: no se encontró un préstamo activo para ese libro.")
        return False

    libro["estado"] = "Disponible"
    prestamo_activo["estado"] = "Devuelto"
    guardar_libros(libros)
    guardar_prestamos(prestamos)
    print("Libro devuelto correctamente.")
    return True


def mostrar_prestamos(prestamos, libros):
    """Muestra número, título, estudiante, fecha y estado de cada préstamo."""
    print("\n" + "=" * 88)
    print(f"{'NÚMERO':<10}{'TÍTULO':<28}{'ESTUDIANTE':<22}{'FECHA':<14}{'ESTADO':<14}")
    print("-" * 88)
    if not prestamos:
        print("No hay préstamos registrados.")
    else:
        for prestamo in prestamos:
            libro = buscar_por_codigo(libros, prestamo["codigo_libro"])
            titulo = libro["titulo"] if libro else "Libro no encontrado"
            print(
                f"{prestamo['numero']:<10}{titulo[:27]:<28}"
                f"{prestamo['estudiante'][:21]:<22}{prestamo['fecha']:<14}"
                f"{prestamo['estado']:<14}"
            )
    print("=" * 88)
    return len(prestamos)


def reporte_general(libros, prestamos):
    """Calcula libros disponibles, prestados, préstamos activos y porcentaje."""
    disponibles = 0
    prestados = 0
    for libro in libros:
        if libro["estado"] == "Disponible":
            disponibles += 1
        elif libro["estado"] == "Prestado":
            prestados += 1

    activos = sum(1 for prestamo in prestamos if prestamo["estado"] == "Activo")
    try:
        porcentaje = (prestados / len(libros)) * 100
    except ZeroDivisionError:
        porcentaje = 0

    print("\n========== REPORTE GENERAL ==========")
    print(f"Libros registrados: {len(libros)}")
    print(f"Libros disponibles: {disponibles}")
    print(f"Libros prestados: {prestados}")
    print(f"Préstamos registrados: {len(prestamos)}")
    print(f"Préstamos activos: {activos}")
    print(f"Porcentaje de libros prestados: {porcentaje:.1f}%")
    print("=====================================")
    return {
        "libros": len(libros),
        "disponibles": disponibles,
        "prestados": prestados,
        "prestamos": len(prestamos),
        "activos": activos,
        "porcentaje_prestados": porcentaje,
    }


def mostrar_menu():
    """Muestra el menú principal."""
    print("""
====================================
       BIBLIOTECA DIGITAL
====================================
1. Registrar libro        5. Devolver libro
2. Mostrar libros         6. Mostrar préstamos
3. Buscar libro           7. Reporte general
4. Prestar libro          8. Salir
====================================""")


def main():
    """Carga los datos y repite el menú hasta que se elija la opción 8."""
    libros = cargar_libros()
    prestamos = cargar_prestamos()
    opcion = 0

    while opcion != 8:
        mostrar_menu()
        opcion = leer_entero("Elija una opción: ")
        if opcion == 1:
            registrar_libro(libros)
        elif opcion == 2:
            mostrar_libros(libros)
        elif opcion == 3:
            buscar_libro(libros)
        elif opcion == 4:
            prestar_libro(libros, prestamos)
        elif opcion == 5:
            devolver_libro(libros, prestamos)
        elif opcion == 6:
            mostrar_prestamos(prestamos, libros)
        elif opcion == 7:
            reporte_general(libros, prestamos)
        elif opcion == 8:
            guardar_libros(libros)
            guardar_prestamos(prestamos)
            print("Datos guardados. ¡Hasta pronto!")
        else:
            print("Opción no válida: elija un número del 1 al 8.")


if __name__ == "__main__":
    main()
