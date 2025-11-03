
import requests  # Para la API
import csv       # Para leer y escribir archivos CSV
import os        # Para ver si el archivo existe 

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

def mostrar_menu_ordenar():
    
    #imprime opciones sub menu ordenar y devuelve string

    print("\n--- Sub-Menu: Ordenar paises ---")
    print("1. Ordenar por nombre")
    print("2. Ordenar por población")
    print("3. Ordenar por Superficie")
    print("4. Volver al menu principal")
    return input("Seleccione una opcion de filtro (1-4): ")

def ordenar_paises(paises):
    while True:
        opc_menu_ordenar = mostrar_menu_ordenar()

        if opc_menu_ordenar == "1":
            
            paises_ordenados = sorted(paises, key=lambda x: x['nombre'].lower())
            print("\n==> Países ordenados por NOMBRE:")
            mostrar_paises(paises_ordenados)

        elif opc_menu_ordenar == "2":

            paises_ordenados = sorted(paises, key=lambda x: x['poblacion'])
            print("\n==> Países ordenados por POBLACIÓN:")
            mostrar_paises(paises_ordenados)

        elif opc_menu_ordenar == "3":
            orden = input("Ingrese si lo quiere en orden ascendente(A) o descendente(D): ").upper().strip()
            while True:
                if orden == "":
                    print("Error! este campo no puede estar vacío")
                    orden = input("Ingrese si lo quiere en orden ascendente(A) o descendente(D): ").upper().strip()
                elif orden != "A" and orden != "D":
                    print("La respuesta que quiere ingresar es inválida")
                    orden = input("Ingrese si lo quiere en orden ascendente(A) o descendente(D): ").upper().strip()
                else:
                    break
            if orden == "A":       

                paises_ordenados = sorted(paises, key=lambda x: x['superficie'])
                print("\n==> Países ordenados por SUPERFICIE:")
                mostrar_paises(paises_ordenados)

            elif orden == "D":

                paises_ordenados = sorted(paises, key=lambda x: x['superficie'], reverse= True)
                print("\n==> Países ordenados por SUPERFICIE:")
                mostrar_paises(paises_ordenados)
            
        elif opc_menu_ordenar == "4":
            print("Volviendo al menu principal...")
            break 

        else:
            print(f"Error: '{opc_menu_ordenar}' no es una opcion valida. Intente de nuevo.")
    
def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos de países cargados.")
        return

    print("\n--- Estadísticas Globales ---")

    # País con mayor y menor población
    pais_mas_poblado = max(paises, key=lambda x: x['poblacion'])
    pais_menos_poblado = min(paises, key=lambda x: x['poblacion'])

    # País con mayor y menor superficie
    pais_mas_grande = max(paises, key=lambda x: x['superficie'])
    pais_mas_chico = min(paises, key=lambda x: x['superficie'])

    # Promedios globales
    prom_poblacion = sum(p['poblacion'] for p in paises) / len(paises)
    prom_superficie = sum(p['superficie'] for p in paises if p['superficie'] > 0) / len([p for p in paises if p['superficie'] > 0])

    print(f"\n Total de países: {len(paises)}")
    print(f" País más poblado: {pais_mas_poblado['nombre']} ({pais_mas_poblado['poblacion']:,} hab.)")
    print(f" País menos poblado: {pais_menos_poblado['nombre']} ({pais_menos_poblado['poblacion']:,} hab.)")
    print(f" País más grande: {pais_mas_grande['nombre']} ({pais_mas_grande['superficie']:,} km²)")
    print(f" País más chico: {pais_mas_chico['nombre']} ({pais_mas_chico['superficie']:,} km²)")
    print(f"Promedio de población: {prom_poblacion:,.0f} hab.")
    print(f" Promedio de superficie: {prom_superficie:,.0f} km²")

    # --- Estadísticas por continente ---
    print("\n--- Estadísticas por Continente ---")
    continentes = {}

    for pais in paises:
        cont = pais['continente']
        if cont not in continentes:
            continentes[cont] = {'poblacion_total': 0, 'superficie_total': 0, 'cantidad': 0}
        continentes[cont]['poblacion_total'] += pais['poblacion']
        continentes[cont]['superficie_total'] += pais['superficie']
        continentes[cont]['cantidad'] += 1

    for cont, datos in continentes.items():
        pobl_prom = datos['poblacion_total'] / datos['cantidad']
        sup_prom = datos['superficie_total'] / datos['cantidad']
        print(f"\n {cont}:")
        print(f"   - Países: {datos['cantidad']}")
        print(f"   - Promedio población: {pobl_prom:,.0f} hab.")
        print(f"   - Promedio superficie: {sup_prom:,.0f} km²")


        

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

            ordenar_paises(paises)  

        elif opcion == '4':
            
            mostrar_estadisticas(paises)
            
        elif opcion == '5':
            print("Gracias por usar el programa. ¡Adios!")
            break 
            
        else:
            print(f"Error: '{opcion}' no es una opcion valida. Intente de nuevo.")

#punto de entrada del programa
if __name__ == "__main__":
    main()