import os
from api import cargar_datos_api
from archivos import cargar_datos_csv, guardar_datos_csv
from menu import mostrar_menu
from validaciones import confirmar_accion
from operaciones import buscar_pais_por_nombre, filtrar_paises, ordenar_paises, mostrar_estadisticas

def main():
    archivo_csv = "paises.csv"
    url_api = "https://restcountries.com/v3.1/all?fields=name,population,area,continents"

    if os.path.exists(archivo_csv):
        paises = cargar_datos_csv(archivo_csv)
    else:
        paises = cargar_datos_api(url_api)
        if paises:
            guardar_datos_csv(paises, archivo_csv)
        else:
            print("No se pudieron obtener los datos.")
            return

    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            buscar_pais_por_nombre(paises, input("Nombre del país: "))
        elif opcion == "2":
            filtrar_paises(paises)
        elif opcion == "3":
            ordenar_paises(paises)
        elif opcion == "4":
            mostrar_estadisticas(paises)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        elif opcion == "6":
            if confirmar_accion("¿Actualizar datos desde la API?"):
                nuevos = cargar_datos_api(url_api)
                if nuevos:
                    guardar_datos_csv(nuevos, archivo_csv)
                    paises = nuevos
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
