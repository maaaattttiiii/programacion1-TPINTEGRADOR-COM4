# main.py
import requests 


def cargar_datos_api(url):
    """
    Carga los datos de los paises desde la API de RestCountries.
    Maneja errores de conexion y de formato de datos.
    Retorna una lista de diccionarios (paises).
    """
    lista_paises = []
    try:
        # 1. Hacemos la peticion GET a la URL
        print("Obteniendo datos desde la API... (esto puede tardar un momento)")
        respuesta = requests.get(url, timeout=10) # timeout de 10 seg
        
        # 2. Verifica si la peticion fue exitosa (codigo 200)
        respuesta.raise_for_status() 
        
        # 3. Convierte la respuesta JSON en una lista de Python
        datos_json = respuesta.json()
        
        print(f"Datos recibidos. Procesando {len(datos_json)} paises...")

        # 4. Iteramos sobre la lista que nos dio la API
        for pais_api in datos_json:
            try:
                # 5. Mapeo (traduccion) de campos
                
                # El nombre comun esta anidado en {'name': {'common': 'Argentina'}}
                nombre = pais_api['name']['common']
                
                poblacion = pais_api['population']
                
                # La API devuelve 'area', nosotros usamos 'superficie'
                # Lo convertimos a int para asegurar que sea un numero
                superficie = int(pais_api.get('area', 0)) # .get('area', 0) es mas seguro
                
                # 'continents' es una lista, ej: ['South America']
                # Tomamos el primero, o 'Indefinido' si la lista esta vacia o no existe
                if pais_api.get('continents'):
                    continente = pais_api['continents'][0]
                else:
                    continente = 'Indefinido'
                
                # [DEBUG] Opcional: imprimir para ver que esta cargando
                # print(f"Cargado: {nombre} ({continente})")

                # 6. Armamos nuestro diccionario estandarizado
                pais = {
                    'nombre': nombre,
                    'poblacion': poblacion,
                    'superficie': superficie,
                    'continente': continente
                }
                lista_paises.append(pais)
                
            except (KeyError, IndexError, TypeError) as e:
                # Si a un pais le falta un dato critico (ej. 'name' o 'population')
                nombre_oficial = pais_api.get('name', {}).get('official', 'Pais desconocido')
                print(f"  -> Datos incompletos para '{nombre_oficial}'. Se omite este pais. (Error: {e})")

    except requests.exceptions.Timeout:
        print(f"Error: La peticion a la API tardo demasiado (timeout).")
        return None
    except requests.exceptions.RequestException as e:
        # Fallo la conexion, la API esta caida, la URL esta mal, etc.
        print(f"Error al conectar con la API: {e}")
        return None # Retornamos None para indicar que fallo la carga
        
    print(f"\nSe cargaron {len(lista_paises)} paises exitosamente desde la API.")
    return lista_paises

def mostrar_menu():
    """
    Imprime las opciones del menu principal en la consola.
    NO recibe parametros.
    RETORNA la opcion elegida por el usuario (como string).
    """
    print("\n--- Menu Principal: Gestion de Paises ---")
    print("1. Buscar un pais por nombre")
    print("2. Filtrar paises")
    print("3. Ordenar paises")
    print("4. Mostrar estadisticas")
    print("5. Salir")
    
    # Pedimos el input DENTRO de la funcion
    opcion_elegida = input("Seleccione una opcion (1-5): ")
    
    # Retornamos el valor
    return opcion_elegida

def mostrar_paises(lista_para_mostrar):
    """
    Imprime una lista de paises de forma ordenada.
    Maneja el caso de una lista vacia.
    """
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

# --- Funciones de Consulta (Requerimiento 2) ---

def buscar_pais_por_nombre(paises, nombre_buscado):
    """
    Busca paises por coincidencia parcial e insensible a mayusculas.
    """
    resultados = []
    
    if not nombre_buscado.strip():
        print("\nError: El termino de busqueda no puede estar vacio.")
        return

    termino_lower = nombre_buscado.lower()
    
    for pais in paises:
        nombre_pais_lower = pais['nombre'].lower()
        if termino_lower in nombre_pais_lower:
            resultados.append(pais)
            
    mostrar_paises(resultados)
    
# --- Funcion Principal (main) ---

def main():
    """
    Funcion principal que ejecuta el programa.
    """
    
    url_api = "https://restcountries.com/v3.1/all?fields=name,population,area,continents"
    paises = cargar_datos_api(url_api)
    
    if paises is None:
        print("No se pudieron cargar los datos. El programa se cerrara.")
        return 

    # Bucle del menu principal
    while True:
        # 1. Llamamos a mostrar_menu() (sin parametros)
        #    y guardamos el string que retorna.
        opcion = mostrar_menu() 
        
        # 2. Comparamos con STRINGS ('1', '2', etc.)
        #    Esto evita que el programa se rompa si el usuario
        #    escribe "hola" (simplemente ira al 'else').
        
        if opcion == '1':
            nombre = input("Ingrese el nombre (o parte) del pais a buscar: ")
            buscar_pais_por_nombre(paises, nombre)
            # 3. YA NO se imprime "pendiente"
        
        elif opcion == '2':
            # [PENDIENTE] llamar a filtrar_paises(paises)
            print("...funcion de filtrado pendiente...")
            
        elif opcion == '3':
            # [PENDIENTE] llamar a ordenar_paises(paises)
            print("...funcion de ordenamiento pendiente...")
            
        elif opcion == '4':
            # [PENDIENTE] llamar a mostrar_estadisticas(paises)
            print("...funcion de estadisticas pendiente...")
            
        elif opcion == '5':
            print("Gracias por usar el programa. ¡Adios!")
            break # Rompe el bucle while True
            
        else:
            print(f"Error: '{opcion}' no es una opcion valida. Intente de nuevo.")

# --- Punto de Entrada del Programa ---
if __name__ == "__main__":
    main()