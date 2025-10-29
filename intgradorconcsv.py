# main.py
import requests  # Para la API
import csv       # Para leer y escribir archivos CSV
import os        # Para ver si el archivo existe 


# MANEJO DE DATOS (API Y CSV)


def cargar_datos_api(url):
   
    # Carga los datos de los paises desde la API 
    
    lista_paises = []
    try:
        print("Obteniendo datos desde la API... (esto puede tardar un momento)")
        respuesta = requests.get(url, timeout=10) 
        respuesta.raise_for_status() 
        datos_json = respuesta.json()
        print(f"Datos recibidos. Procesando {len(datos_json)} paises...")

        for pais_api in datos_json:
            try:
                nombre = pais_api['name']['common']
                poblacion = pais_api['population']
                superficie = int(pais_api.get('area', 0))
                continente = pais_api['continents'][0] if pais_api.get('continents') else 'Indefinido'

                pais = {
                    'nombre': nombre,
                    'poblacion': poblacion,
                    'superficie': superficie,
                    'continente': continente
                }
                lista_paises.append(pais)
                
            except (KeyError, IndexError, TypeError):
                nombre_oficial = pais_api.get('name', {}).get('official', 'Pais desconocido')
                print(f"  -> Datos incompletos para '{nombre_oficial}'. Se omite este pais.")

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None 
        
    print(f"Se procesaron {len(lista_paises)} paises exitosamente desde la API.")
    return lista_paises

def guardar_datos_csv(paises, ruta_archivo): #guarda la lista de paises 
    
    if not paises:
        print("No hay paises para guardar.")
        return

    # definimos los titulos para el csv
    cabeceras = ['nombre', 'poblacion', 'superficie', 'continente']
    
    try:
        #abrimos el archivo en modo escritura y ponemos el newline para evitar lineas en blanco
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            # Usamos DictWriter para listas de diccionarios
            escritor_csv = csv.DictWriter(archivo, fieldnames=cabeceras)
             
            escritor_csv.writeheader()
            
            escritor_csv.writerows(paises)      
        print(f"Datos guardados exitosamente en '{ruta_archivo}'")
        
    except IOError as e: 
        print(f"Error al escribir el archivo CSV: {e}")
    except Exception as e:
        print(f"Ocurrio un error inesperado al guardar el CSV: {e}")

def cargar_datos_csv(ruta_archivo):

    #Carga los datos de los paises desde el CSV
    #Retorna una lista de diccionarios (paises).
    
    lista_paises = []
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            # Usamos DictReader para leer el CSV como diccionarios
            lector_csv = csv.DictReader(archivo)
            
            for fila in lector_csv:
                try:
                    pais = {
                        'nombre': fila['nombre'],
                        'poblacion': int(fila['poblacion']),
                        'superficie': int(fila['superficie']),
                        'continente': fila['continente']
                    }
                    lista_paises.append(pais)
                except ValueError:
                    print(f"Error de formato en la linea del CSV: {fila}. Se omite.")
                except KeyError:
                    print(f"Error de columnas en el CSV: {fila}. Faltan datos. Se omite.")
                    
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo en la ruta '{ruta_archivo}'")
        return None 
    except Exception as e:
        print(f"Ocurrio un error inesperado al cargar el CSV: {e}")
        return None
        
    print(f"Se cargaron {len(lista_paises)} paises exitosamente desde '{ruta_archivo}'.")
    return lista_paises

# INTERFAZ Y FUNCIONALIDADES

def mostrar_menu(): #le mostramos el menú al usuario

    print("\n--- Menu Principal: Gestion de Paises ---")
    print("1. Buscar un pais por nombre")
    print("2. Filtrar paises")
    print("3. Ordenar paises")
    print("4. Mostrar estadisticas")
    print("5. Salir")
    return input("Seleccione una opcion (1-5): ")

def mostrar_menu_filtrado():
    """
    Imprime las opciones del sub-menu de filtros y retorna la opcion (string).
    """
    print("\n--- Sub-Menu: Filtrar Paises ---")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Poblacion")
    print("3. Filtrar por Rango de Superficie")
    print("4. Volver al menu principal")
    return input("Seleccione una opcion de filtro (1-4): ")

def filtrar_paises(paises):

    while True:
        #sub menu para las opciones del filtro
        opcion_filtro = mostrar_menu_filtrado()
        
        resultados = [] #lista para los paises que vayamos filtrando

        if opcion_filtro == '1':
            continente_buscado = input("Ingrese el nombre del continente: ")
            
            if not continente_buscado.strip():
                print("Error: El nombre del continente no puede estar vacio.")
                continue

            termino_lower = continente_buscado.lower()
            
            for pais in paises:
                if termino_lower == pais['continente'].lower():
                    resultados.append(pais)
            
            mostrar_paises(resultados)

        elif opcion_filtro == '2':
            print("--- Filtro por Poblacion ---")
            
            #usamos la función aux para evitar los errores
            min_poblacion = validar_num("Ingrese la poblacion MINIMA: ")
            max_poblacion = validar_num("Ingrese la poblacion MAXIMA: ")

            if min_poblacion > max_poblacion:
                print("Error: La poblacion minima no puede ser mayor a la maxima.")
                continue # Vuelve al inicio del bucle
                
            for pais in paises:
                poblacion_pais = pais['poblacion']
                # Verificamos si la poblacion esta DENTRO del rango
                if min_poblacion <= poblacion_pais <= max_poblacion:
                    resultados.append(pais)
            
            mostrar_paises(resultados)

        elif opcion_filtro == '3':
            # --- FILTRAR POR RANGO DE SUPERFICIE ---
            # Esta logica es identica a la de Poblacion
            print("--- Filtro por Superficie (km2) ---")
            
            min_superficie = validar_num("Ingrese la superficie MINIMA: ")
            max_superficie = validar_num("Ingrese la superficie MAXIMA: ")

            if min_superficie > max_superficie:
                print("Error: La superficie minima no puede ser mayor a la maxima.")
                continue 
                
            for pais in paises:
                superficie_pais = pais['superficie']
                if min_superficie <= superficie_pais <= max_superficie:
                    resultados.append(pais)
            
            mostrar_paises(resultados)

        elif opcion_filtro == '4':
            print("Volviendo al menu principal...")
            break 

        else:
            print(f"Error: '{opcion_filtro}' no es una opcion valida. Intente de nuevo.")

#funciones aux para las validaciones

def validar_num(mensaje):
    while True:
        texto_ingresado = input(mensaje)
        try:
            # Intentamos convertir el texto a un numero entero
            numero = int(texto_ingresado)
            
            # Verificamos que no sea negativo
            if numero < 0:
                print("Error: El numero no puede ser negativo. Intente de nuevo.")
            else:
                # Si todo salio bien, rompemos el bucle y retornamos
                return numero 
                
        except ValueError:
            # Si int(texto_ingresado) falla, se ejecuta esto
            print(f"Error: '{texto_ingresado}' no es un numero valido. Intente de nuevo.")

def mostrar_paises(lista_para_mostrar): #muestra los paises de forma ordenada

    if not lista_para_mostrar:
        print("\n==> No se encontraron paises que cumplan con el criterio.")
        return

    print(f"\n--- {len(lista_para_mostrar)} Paises Encontrados ---")
    for pais in lista_para_mostrar:
        print(f"- Nombre:     {pais['nombre']}")
        print(f"  Poblacion:  {pais['poblacion']:>15,}")
        print(f"  Superficie: {pais['superficie']:>15,} km2")
        print(f"  Continente: {pais['continente']}")
        print("-" * 20) 

def buscar_pais_por_nombre(paises, nombre_buscado):
    resultados = []
    if not nombre_buscado.strip():
        print("\nError: El termino de busqueda no puede estar vacio.")
        return

    termino_lower = nombre_buscado.lower()
    for pais in paises:
        if termino_lower in pais['nombre'].lower():
            resultados.append(pais)
            
    mostrar_paises(resultados)
    
#  EJECUCION PRINCIPAL

def main():
    
    # Definimos los archivos y URL
    archivo_csv = 'paises.csv'
    url_api = "https://restcountries.com/v3.1/all?fields=name,population,area,continents"
    
    paises = None 

    # Comprobamos si el archivo CSV ya existe
    if os.path.exists(archivo_csv):
        # Si existe, cargamos desde el CSV
        print(f"Archivo '{archivo_csv}' encontrado.")
        paises = cargar_datos_csv(archivo_csv)
    else:
        # Si NO existe, descargamos desde la API
        print(f"Archivo '{archivo_csv}' no encontrado.")
        paises_api = cargar_datos_api(url_api)
        
       
        if paises_api:
        
            guardar_datos_csv(paises_api, archivo_csv)
            
            paises = paises_api
        else:
            print("Fallo la obtencion de datos de la API.")
    

    
    # Si paises es None fallo la carga CSV o la API
    if paises is None:
        print("No se pudieron cargar los datos. El programa se cerrara.")
        return 

    while True:
        opcion = mostrar_menu() 
        
        if opcion == '1':
            nombre = input("Ingrese el nombre (o parte) del pais a buscar: ")
            buscar_pais_por_nombre(paises, nombre)
        
        elif opcion == '2':

            filtrar_paises(paises)
            
        elif opcion == '3':
            # [PENDIENTE]
            print("...funcion de ordenamiento pendiente...")
            
        elif opcion == '4':
            # [PENDIENTE]
            print("...funcion de estadisticas pendiente...")
            
        elif opcion == '5':
            print("Gracias por usar el programa. ¡Adios!")
            break 
            
        else:
            print(f"Error: '{opcion}' no es una opcion valida. Intente de nuevo.")

# --- Punto de Entrada del Programa ---
if __name__ == "__main__":
    main()