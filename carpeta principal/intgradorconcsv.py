
import requests  # Para la API
import csv       # Para leer y escribir archivos CSV
import os        # Para ver si el archivo existe 
import funciones as f
print(dir(f))

    
#  EJECUCION PRINCIPAL

def main():
    
    archivo_csv = 'paises.csv'
    url_api = "https://restcountries.com/v3.1/all?fields=name,population,area,continents"
    
    paises = None 

    # Comprobamos si el archivo CSV ya existe
    if os.path.exists(archivo_csv):
        # Si existe, cargamos desde el CSV
        print(f"Archivo '{archivo_csv}' encontrado.")
        paises = f.cargar_datos_csv(archivo_csv)
    else:
        # Si NO existe, descargamos desde la API
        print(f"Archivo '{archivo_csv}' no encontrado.")
        paises_api = f.cargar_datos_api(url_api)
        
       
        if paises_api:
        
            f.guardar_datos_csv(paises_api, archivo_csv)
            
            paises = paises_api
        else:
            print("Fallo la obtencion de datos de la API.")
    

    
    # Si paises es None fallo la carga CSV o la API
    if paises is None:
        print("No se pudieron cargar los datos. El programa se cerrara.")
        return 

    while True:
        opcion = f.mostrar_menu() 
        
        if opcion == '1':
            nombre = input("Ingrese el nombre (o parte) del pais a buscar: ")
            f.buscar_pais_por_nombre(paises, nombre)
        
        elif opcion == '2':

            f.filtrar_paises(paises)
            
        elif opcion == '3':

            f.ordenar_paises(paises)  

        elif opcion == '4':
            
            f.mostrar_estadisticas(paises)
            
        elif opcion == '5':
            print("Gracias por usar el programa. ¡Adios!")
            break 
            
        else:
            print(f"Error: '{opcion}' no es una opcion valida. Intente de nuevo.")

#punto de entrada del programa
if __name__ == "__main__":
    main()