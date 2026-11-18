# Sistema de Biblioteca - POO II

## Ejecución

Desde esta carpeta, ejecutar:

```text
python biblioteca.py
```

El programa crea o actualiza `libros.txt` y `prestamos.txt` en la misma carpeta. Los datos se cargan al iniciar y se guardan al registrar, prestar, devolver o salir.

## Requisitos de la guía cubiertos

- Menú de 8 opciones con `while`, que termina con la opción 8.
- Libros y préstamos representados como diccionarios dentro de listas.
- Una función por opción del menú, con parámetros y `return`.
- Validación de números con `try/except ValueError`.
- Validación de textos vacíos y de comas.
- Archivos de texto con campos separados por comas.
- Manejo de `FileNotFoundError`, `ValueError` y `ZeroDivisionError`.
- Búsqueda sin distinguir mayúsculas y reglas de disponibilidad.

## Secuencia de pruebas solicitada

1. En el menú, escribir una letra y luego `9`. Deben aparecer mensajes de error y el programa debe continuar.
2. Registrar `Clean Code` de Robert Martin y `Estructuras de datos` de Luis Joyanes. Recibirán los códigos 4 y 5.
3. Intentar registrar un título vacío y un título con coma.
4. Buscar `java` y después una palabra que no exista.
5. Prestar los libros 1, 4 y 5 a estudiantes distintos. Intentar prestar otra vez el libro 1 y el código 99.
6. Devolver el libro 4. Intentar devolver el libro 2, que no está prestado.
7. Ejecutar las opciones 2, 6 y 7, y después salir con la opción 8.
8. Volver a ejecutar el programa y elegir la opción 7. El reporte debe conservar los datos guardados.

Después de completar esa secuencia, el reporte esperado es: 5 libros, 3 disponibles, 2 prestados, 3 préstamos registrados, 2 activos y 40.0% de libros prestados.
