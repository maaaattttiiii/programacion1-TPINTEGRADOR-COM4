import requests #sirve para obtener los datos de la API
import csv #para trabajar con el archivo csv
import os #para verificar la exitencia del csv


#pedimos los datos a la API con get 
def cargar_datos_api(url):
    lista_paises = []
    try:
        print("Obteniendo datos desde la API... (esto puede tardar un momento)")
        respuesta = requests.get(url, timeout=10)# esto es para que si no hay respuesta en 10 seg se cancela
        respuesta.raise_for_status()
        datos_json = respuesta.json()# en esta parte la respuesta que viene en formato .json la transformamos en una lista de diccionarios
        print(f"Datos recibidos,{len(datos_json)} países")

        for pais_api in datos_json:
            try:
                name_data = pais_api.get("name", {})
                native_names = name_data.get("nativeName", {})
                if "spa" in native_names:
                    nombre = native_names["spa"].get("common", name_data.get("common"))
                else:
                    nombre = name_data.get("common", "Desconocido")
                poblacion = pais_api.get("population", 0)
                superficie = int(pais_api.get("area", 0))
                continente = pais_api.get("continents", ["Indefinido"])[0]
                pais = {
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente
                }
                lista_paises.append(pais)
            except (KeyError, IndexError, TypeError):
                nombre_oficial = pais_api.get("name", {}).get("official", "Pais desconocido")
                print(f"  -> Datos incompletos para '{nombre_oficial}'. Se omite este país.")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None
    print(f"Se procesaron {len(lista_paises)} países exitosamente desde la API.")
    return lista_paises

def guardar_datos_csv(paises, ruta_archivo):
    if not paises:
        print("No hay países para guardar.")
        return
    cabeceras = ["nombre", "poblacion", "superficie", "continente"]
    try:
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8-sig") as archivo:# modo w abre o crea archivo csv
            escritor_csv = csv.DictWriter(archivo, fieldnames=cabeceras)# escribe lista de diccionarios en el csv
            escritor_csv.writeheader()# primera fila con los nombres de las columnas 
            escritor_csv.writerows(paises)# escribe los paises 
        print(f"Datos guardados exitosamente en '{ruta_archivo}'")
    except IOError as e: #si no se abre o no se escribe salta este error 
        print(f"Error al escribir el archivo CSV: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al guardar el CSV: {e}")

def cargar_datos_csv(ruta_archivo):
    lista_paises = []
    try:
        with open(ruta_archivo, mode="r", encoding="utf-8-sig") as archivo:
            lector_csv = csv.DictReader(archivo)#convierte las filas en diccionario
            for fila in lector_csv:
                try:
                    pais = {
                        "nombre": fila["nombre"],
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"]
                    }
                    lista_paises.append(pais)
                except ValueError:
                    print(f"Error de formato en la línea del CSV: {fila}. Se omite.")
                except KeyError:
                    print(f"Error de columnas en el CSV: {fila}. Faltan datos. Se omite.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado al cargar el CSV: {e}")
        return None
    print(f"Se cargaron {len(lista_paises)} países exitosamente desde '{ruta_archivo}'.")
    return lista_paises


#muestra el menu principal
def mostrar_menu():
    print("\n--- Menú Principal: Gestión de Países ---")
    print("1. Buscar un país por nombre")
    print("2. Filtrar países")
    print("3. Ordenar países")
    print("4. Mostrar estadísticas")
    print("5. Salir")
    print("6. Actualizar datos desde la API")
    return input("Seleccione una opción (1-6): ")

def mostrar_menu_filtrado():
    print("\nSubMenu: Filtrar Países")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Población")
    print("3. Filtrar por Rango de Superficie")
    print("4. Volver al menú principal")
    return input("Seleccione una opción de filtro (1-4): ")

def filtrar_paises(paises):
    while True:
        opcion_filtro = mostrar_menu_filtrado()
        resultados = []# se crea lista vacia para que no salte errores 
        if opcion_filtro == "1":
            continente_buscado = input("Ingrese el nombre del continente: ").strip()
            if not continente_buscado:
                print("Error: El nombre del continente no puede estar vacío.")
                continue
            for pais in paises:
                if continente_buscado.lower() == pais["continente"].lower():
                    resultados.append(pais)
            mostrar_paises(resultados)#para imprimir resultados

        elif opcion_filtro == "2":
            print("--- Filtro por Población ---")
            min_poblacion = validar_num("Ingrese la población MÍNIMA: ")
            max_poblacion = validar_num("Ingrese la población MÁXIMA: ")
            if min_poblacion > max_poblacion:
                print("Error: La población mínima no puede ser mayor a la máxima.")
                continue
            for pais in paises:
                if min_poblacion <= pais["poblacion"] <= max_poblacion:
                    resultados.append(pais)
            mostrar_paises(resultados)

        elif opcion_filtro == "3":
            print("--- Filtro por Superficie (km²) ---")
            min_superficie = validar_num("Ingrese la superficie MÍNIMA: ")
            max_superficie = validar_num("Ingrese la superficie MÁXIMA: ")
            if min_superficie > max_superficie:
                print("Error: La superficie mínima no puede ser mayor a la máxima.")
                continue
            for pais in paises:
                if min_superficie <= pais["superficie"] <= max_superficie:
                    resultados.append(pais)
            mostrar_paises(resultados)

        elif opcion_filtro == "4":
            print("Volviendo al menú principal...")
            break
        else:
            print(f"Error: '{opcion_filtro}' no es una opción válida.")

def mostrar_menu_ordenar():
    print("\nSub-Menu: Ordenar Países")
    print("1. Ordenar por nombre")
    print("2. Ordenar por población")
    print("3. Ordenar por superficie")
    print("4. Volver al menú principal")
    return input("Seleccione una opción (1-4): ")

def ordenar_paises(paises):
    while True:
        #en las opciones usamos lambda para los criterios del sorted
        opc = mostrar_menu_ordenar()
        if opc == "1":
            paises_ordenados = sorted(paises, key=lambda x: x["nombre"].lower())#sorted ordena segun criterios
            mostrar_paises(paises_ordenados)
        elif opc == "2":
            paises_ordenados = sorted(paises, key=lambda x: x["poblacion"])
            mostrar_paises(paises_ordenados)
        elif opc == "3":
            orden = input("Ascendente (A) o Descendente (D): ").upper().strip()
            while orden not in ("A","D"):
                print("Respuesta inválida.")
                orden = input("Ascendente (A) o Descendente (D): ").upper().strip()
            paises_ordenados = sorted(paises, key=lambda x: x["superficie"], reverse=(orden=="D"))
            mostrar_paises(paises_ordenados)
        elif opc == "4":
            break
        else:
            print(f"Error: '{opc}' no es una opción válida.")

def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos cargados.")
        return
    pais_mas_poblado = max(paises, key=lambda x: x["poblacion"])
    pais_menos_poblado = min(paises, key=lambda x: x["poblacion"])
    pais_mas_grande = max(paises, key=lambda x: x["superficie"])
    pais_mas_chico = min(paises, key=lambda x: x["superficie"])
    prom_poblacion = sum(p["poblacion"] for p in paises)/len(paises)
    prom_superficie = sum(p["superficie"] for p in paises if p["superficie"]>0)/len([p for p in paises if p["superficie"]>0])
    print(f"\nTotal de países: {len(paises)}")
    print(f"País más poblado: {pais_mas_poblado['nombre']} ({pais_mas_poblado['poblacion']:,} hab.)")
    print(f"País menos poblado: {pais_menos_poblado['nombre']} ({pais_menos_poblado['poblacion']:,} hab.)")
    print(f"País más grande: {pais_mas_grande['nombre']} ({pais_mas_grande['superficie']:,} km2)")
    print(f"País más chico: {pais_mas_chico['nombre']} ({pais_mas_chico['superficie']:,} km2)")
    print(f"Promedio de población: {prom_poblacion:,.0f} hab.")
    print(f"Promedio de superficie: {prom_superficie:,.0f} km2")
    continentes = {}
    for pais in paises:
        cont = pais["continente"]
        if cont not in continentes:
            continentes[cont] = {"poblacion_total":0,"superficie_total":0,"cantidad":0}
        continentes[cont]["poblacion_total"]+=pais["poblacion"]
        continentes[cont]["superficie_total"]+=pais["superficie"]
        continentes[cont]["cantidad"]+=1
    for cont, datos in continentes.items():
        pobl_prom = datos["poblacion_total"]/datos["cantidad"]
        sup_prom = datos["superficie_total"]/datos["cantidad"]
        print(f"\n{cont}:")
        print(f"  Países: {datos['cantidad']}")
        print(f"  Promedio población: {pobl_prom:,.0f} hab.")
        print(f"  Promedio superficie: {sup_prom:,.0f} km²")

def validar_num(mensaje):#funcion para validar las entradas de datos numericos
    while True:
        texto = input(mensaje)
        try:
            num = int(texto)
            if num<0:
                print("No puede ser negativo.")
            else:
                return num
        except ValueError:
            print("Debe ingresar un número válido.")

def mostrar_paises(lista):# va mostrando los paises que cumplan los criterios en los que se usen 
    if not lista:
        print("\nNo se encontraron países que cumplan el criterio.")
        return
    print(f"\n--- {len(lista)} Países Encontrados ---")
    for p in lista:
        print(f"- {p['nombre']}")
        print(f"  Población:  {p['poblacion']:,}")
        print(f"  Superficie: {p['superficie']:,} km2")
        print(f"  Continente: {p['continente']}")
        print("-"*20)

def buscar_pais_por_nombre(paises,nombre):
    if not nombre.strip():
        print("Este campo no puede estar vacío.")
        return
    resultados = [p for p in paises if nombre.lower() in p["nombre"].lower()]
    mostrar_paises(resultados)

def confirmar_accion(mensaje):# devuelve bool 
    while True:
        resp = input(f"{mensaje} (S/N): ").strip().upper()
        if resp=="S":
            return True
        elif resp=="N":
            return False
        else:
            print("Ingrese 'S' para Sí o 'N' para No.")



# principal 

def main():
    archivo_csv = "paises.csv"
    url_api = "https://restcountries.com/v3.1/all?fields=name,population,area,continents"
    paises = None
    if os.path.exists(archivo_csv):
        print(f"Archivo '{archivo_csv}' encontrado.")
        paises = cargar_datos_csv(archivo_csv)
    else:
        print(f"Archivo '{archivo_csv}' no encontrado.")
        paises_api = cargar_datos_api(url_api)
        if paises_api:
            guardar_datos_csv(paises_api, archivo_csv)
            paises = paises_api
        else:
            print("Fallo la obtención de datos de la API.")
    if paises is None:
        print("No se pudieron cargar los datos. El programa se cerrará.")
        return
    while True:
        opcion = mostrar_menu()
        if opcion=="1":
            nombre = input("Ingrese el nombre (o parte) del país a buscar: ")
            buscar_pais_por_nombre(paises,nombre)
        elif opcion=="2":
            filtrar_paises(paises)
        elif opcion=="3":
            ordenar_paises(paises)
        elif opcion=="4":
            mostrar_estadisticas(paises)
        elif opcion=="5":
            print("Gracias por usar el programa, sos tremendo crack, espero que te vaya muy bien")
            break
        elif opcion=="6":
            if confirmar_accion("¿Desea actualizar los datos desde la API? se cambiará el csv actual"):
                nuevos_datos = cargar_datos_api(url_api)
                if nuevos_datos:
                    guardar_datos_csv(nuevos_datos, archivo_csv)
                    paises = nuevos_datos
                    print("Los datos fueron actualizados correctamente.")
                else:
                    print("No se pudo actualizar desde la API.")
            else:
                print("Actualización cancelada.")
        else:
            print(f"Error: '{opcion}' no es una opción válida.")

if __name__=="__main__":
    main()

