from collections import deque #Permite insertar y eliminar elementoos al principio/fin de una lista
from io import open #Abrir archivos compatibles con python
import os  #Verificacion de archivos
import re  #Validar patrones de texto
import random #Numeros aleatorios 

archivo = "usuarios.txt"
ninjas_archivo = "ninjas.txt"
habilidades = "habilidades_ninja.txt"
usuarios = []
arboles_ninja = {}

#crear arbol de habilidades de cada ninja
class NodoHabilidad:
    def __init__(self, nombre, puntos):
        self.nombre = nombre
        self.puntos = puntos
        self.izq = None
        self.der = None

def sumar_habilidades(nodo):
    if nodo is None:
        return 0
    return (nodo.puntos + sumar_habilidades(nodo.izq) + sumar_habilidades(nodo.der))

def crear_arbol_personalizado(nombre_ninja):
    print(f"\n--- Asignar habilidades a {nombre_ninja} ---")
    habilidades = []
    for i in range(1, 5):
        habilidad = input(f"Ingrese habilidad {i}: ").strip()
        habilidades.append(habilidad)

    raiz = NodoHabilidad(habilidades[0], random.randint(5, 10))
    raiz.izq = NodoHabilidad(habilidades[1], random.randint(5, 10))
    raiz.der = NodoHabilidad(habilidades[2], random.randint(5, 10))
    raiz.izq.izq = NodoHabilidad(habilidades[3], random.randint(5, 10))

    return raiz
ninjas =[]


def mostrar_habilidades(nodo, nivel=0):
    if nodo:
        print("  " * nivel + f"{nodo.nombre} {nodo.puntos}")
        mostrar_habilidades(nodo.izq, nivel + 1)
        mostrar_habilidades(nodo.der, nivel + 1)    


#ROL ADMINISTRADOR 
def login_administrador():
    nombre = "admin"
    pasword ="admin123"
    print("Inicio de sesion del administrador")
    while True:
        usuario = input("Usuario: ")
        contraseña = input("Contraseña: ")
        if usuario == nombre and contraseña == pasword:
            print("Acceso permitido")
            break
        else:
            print("Acceso denegado")

def menu_administrador():
    print("-----MENU ADMINISTRADOR-----")
    print("1. Agregar nuevos ninjas")
    print("2. Listar ninjas")
    print("3. Consultar ninja")
    print("4. Actualizar atributos de un ninja")
    print("5. Eliminar ninja")
    print("6. Crear arbol de habilidades ninja")
    print("7. Guardar cambios")
    print("0. Salir")

def leer_ninjas():
    ninjas = []
    if not os.path.exists(ninjas_archivo):
        return ninjas
    with open(ninjas_archivo, "r", encoding= "utf-8") as f:
        for l in f:
            datos = l.strip().split(",")
            if len(datos) == 4:
                ninjas.append({
                    "Nombre": datos[0],
                    "Puntos": int(datos[1]),
                    "Estilo": datos[2],
                    "Rango": datos[3]
                })
    return ninjas 


def guardar_ninjas(lista_ninjas):
    try:
        with open(ninjas_archivo, "w",encoding="utf-8") as f:
            for n in lista_ninjas:
                f.write(f"{n['Nombre']},{n['Puntos']},{n['Estilo']},{n['Rango']}\n")
        print("Ninjas guardados correctamente")
    except Exception as e:
        print(f"Error al guardar ninja: {e}")

def agregar_ninja(nuevo_ninja):
    nombre = input("Nombre del ninja: ")
    puntos = random.randint(10,20)
    estilo = input("Estilo de pelea: ")
    rango = input("Rango: ")
    nuevo_ninja.append({
        "Nombre": nombre,
        "Puntos": puntos,
        "Estilo": estilo,
        "Rango": rango
    })
    print("Ninja agregado")

def listar_ninjas(lista_ninjas):
    if not lista_ninjas:
        print("No existen registro de ninjas")
        return
    while True:
        ordenamiento = input("Ordenar por (nombre o puntos): ").strip().lower()
        if ordenamiento != "nombre" and ordenamiento != "puntos":
            print("No fue posible ordenar. Ingrese (nombre o puntos):")
        else:
            break
    if ordenamiento == "nombre":
        lista_ordenada = sorted(lista_ninjas, key=lambda p:p['Nombre'])
    else: 
        lista_ordenada = sorted(lista_ninjas, key=lambda n:n['Puntos'],reverse=True)
    print("\nLista de ninjas")
    for ninja in lista_ordenada:
        print(f"{ninja['Nombre']} | {ninja['Puntos']} | {ninja['Estilo']} | {ninja['Rango']}")

def buscar_ninja(lista_ninjas):
    if not lista_ninjas:
        print("No hay ninjas registrados")
        return 
    while True:
        buscar_campo = input("¿Desea buscar por 'nombre' o 'estilo'?: ").strip().lower()
        if buscar_campo != "nombre" and buscar_campo != "estilo":
            print("Opcion no valida.Intente nuevamente: ")
        else: 
            break
    
    clave_directa = {"nombre": "Nombre", "estilo":"Estilo"}
    real_campo = clave_directa[buscar_campo]

    clave_a_buscar = input(f"Ingrese el {buscar_campo} exacto a buscar: ").strip().lower()
    lista_ninjas.sort(key=lambda n:n[real_campo].lower())
    valores = [ninja[real_campo].lower() for ninja in lista_ninjas]

    #Busqueda binaria
    izq = 0
    der = len(valores)-1
    while izq <= der:
        med = (izq + der) // 2
        if valores[med] == clave_a_buscar:
            print("🥷Ninja encontrado")
            n = lista_ninjas[med]
            print(f"{n['Nombre']} | {n['Puntos']} | {n['Estilo']} | {n['Rango']}\n")
            return
        elif clave_a_buscar < valores[med]:
            der = med - 1
        else: 
            izq = med + 1
    print("No se encontro ninja")

def ninja_a_actualizar(lista_de_ninjas):
    nombre = input("Ingrese el nombre del ninja a actualizar: ").strip()
    for ninja in lista_de_ninjas:
        if ninja['Nombre'].lower() == nombre.lower():
            print(f"Ninja encontrado: {ninja}")
            estilo_nuevo = input("Ingrese el nuevo estilo de pelea: ")
            rango_nuevo = input("Ingrese el nuevo rango (Si desea mantener el rango presione enter): ")
            if estilo_nuevo:
                ninja['Estilo'] = estilo_nuevo
            if rango_nuevo:
                ninja ['Rango'] = rango_nuevo
            print("🥷✅El ninja ha sido actuaizado correctamente")
            return
    print("🥷❎Ninja no encontrado")
    
def eliminar_ninja(lista_de_ninjas):
    nombre_eliminar = input("Ingrese el nombre del ninja a eliminar: ").strip()
    for ninja in lista_de_ninjas:
        if ninja['Nombre'].lower() == nombre_eliminar.lower():
            lista_de_ninjas.remove(ninja)
            print(f"🚯El ninja '{nombre_eliminar}' eliminado correctamente.")
            return
    print("🥷❎Ninja no encontrado. Error al eliminar ninja")
def crear_arbol_para_ninja():
    nombre = input("Nombre del ninja para asignar habilidades: ").strip()
    if nombre == "":
        print("Nombre inválido.")
        return
    arbol = crear_arbol_personalizado(nombre)
    arboles_ninja[nombre] = arbol
    print(f"Arbol de habilidades creado y guardado para {nombre}.")

def guardar_habilidades_ninja(habilidades):
    try:
        with open(habilidades, "w", encoding="utf-8") as f:
            for nombre, arbol in arboles_ninja.items():
                f.write(f"{nombre}\n")
                mostrar_habilidades(arbol, nivel=1)
        print("Habilidades guardadas correctamente.")
    except Exception as e:
        print(f"Error al guardar habilidades: {e}")

def guardar_cambios_en_archivo_original():
    try:
        with open(ninjas_archivo, "w", encoding="utf-8") as f:
            for nombre, arbol in arboles_ninja.items():
                f.write(f"{nombre}\n")
                mostrar_habilidades(arbol, nivel=1)
        print("Cambios guardados correctamente.")
    except Exception as e:
        print(f"Error al guardar cambios: {e}")

#ROL JUGADOR
def menu_jugador():
    print("-----MENU JUGADOR-----")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Ver arbol de habilidades ninja")
    print("4. Simular combate 1 vs 1")
    print("5. Simular rondas del torneo")
    print("6. Consultar ranking")
    print("Guardar progreso")
    print("0. Salir")

def validar_correo(correo):
    patron = r"^[a-zA-Z]+\.[a-zA-Z]+@gmail\.com$"
    return re.match(patron,correo)

def guardar_usuario(nuevo_archivo,lista_usuarios):
    try:
        with open(nuevo_archivo, "w", encoding="utf-8") as f:
            for usuario in lista_usuarios:
                f.write(f"{usuario['Nombre']},{usuario['Identificacion']},{usuario['Edad']},{usuario['Usuario']},{usuario['Contraseña']}\n")
            print("Archivo guardado correctamente")
    except Exception as n:
        print(f"Error al guardar archivo: {n}") 

def verificar_credencial(usuario,contraseña,lista_usuarios):
    if not lista_usuarios:
        print("No existen credenciales.")
        return False
    for u in lista_usuarios:
        if u['Usuario'] == usuario and u['Contraseña'] == contraseña:
            return True
    return False

def agregar_usuario(nuevos_usuarios):
    nombre = input("Nombre Completo: ")
    while True:
        identificacion = input("Identificacion: ")
        if len(identificacion) > 10:
            print("Identificacion no valida: ")
        else:
            break
    while True:
        edad = int(input("Edad: "))
        if edad < 0 or edad > 100:
            print("Ingrese una edad valida.")
        else:
             break
    while True:
        correo = input("Correo (formato: nombre.apellido@gmail.com): ")
        if validar_correo(correo):
            break
        else:
            print("Correo no valido.")
    while True:
        contraseña = input("Contraseña (Minimo 8 caracteres, 1 mayúscula, 1 número): ")
        if len(contraseña) >= 8 and any(c.isupper() for c in contraseña) and any(c.isdigit() for c in contraseña):
            break
        else:
            print("Contraseña corta.")
    nuevos_usuarios.append({
        "Nombre": nombre,
        "Identificacion": identificacion,
        "Edad": edad,
        "Usuario": correo,
        "Contraseña": contraseña
    })
    guardar_usuario(archivo,nuevos_usuarios)

def usuarios_registrados():
    lista_usuarios = []
    if not os.path.exists(archivo):
        print("No existen usuarios registrados")
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        for line in f :
            datos = line.strip().split(",")
            if len(datos) == 5:
                lista_usuarios.append({
                    "Nombre": datos[0],
                    "Identificacion": datos[1],
                    "Edad": datos[2],
                    "Usuario": datos[3],
                    "Contraseña": datos[4]
                })
    return lista_usuarios

def iniciar_sesion(iniciar):
    correo = input("Correo: ")
    contraseña = input("Contraseña: ")
    if verificar_credencial(correo, contraseña, iniciar):
        print(f"Sesion iniciada como {correo}")
        return correo
    else:
        print("No se pudo iniciar sesion. Usuario o contraseña incorrecta")
        return None
    
def ver_arbol_jugador():
    if not arboles_ninja:
        print("No hay árboles de habilidades disponibles.")
        return
    
    print("\nNinjas con habilidades disponibles:")
    for i, nombre in enumerate(arboles_ninja.keys(), 1):
        print(f"{i}. {nombre}")
    
    try:
        seleccion = int(input("Seleccione un ninja por número: "))
        nombres = list(arboles_ninja.keys())
        if 1 <= seleccion <= len(nombres):
            ninja_seleccionado = nombres[seleccion - 1]
            print(f"\nÁrbol de habilidades de {ninja_seleccionado}:")
            mostrar_habilidades(arboles_ninja[ninja_seleccionado])
        else:
            print("No valido. Intenta de nuevo")
    except:
        print("Entrada no válida.")

ninjas_pelea = {nombre: crear_arbol_personalizado(nombre) for nombre in ninjas} 
#simular rondas del torneo
def ronda(nombre_ronda,participantes, ninjas_pelea):
    print(f"{nombre_ronda.upper()} {len(participantes)} ninjas")
    cola = deque(participantes)
    siguiente_ronda = []
    while len(cola) > 0:
        ninja1 = cola.popleft()
        ninja2 = cola.popleft()

        print(f"{ninja1} vs {ninja2}")
        puntos1 = sumar_habilidades(ninjas_pelea[ninja1])
        puntos2 = sumar_habilidades(ninjas_pelea[ninja2])

        print(f"Puntos de {ninja1}: {puntos1}")
        print(f"Puntos de {ninja2}: {puntos2}")
        
        if puntos1 > puntos2:
            ganador = ninja1
        elif puntos2 > puntos1:
            ganador = ninja2
        else:
            ganador = random.choice([ninja1, ninja2])

        print(f"Ganador: {ganador} \n")
        siguiente_ronda.append(ganador)
    return   siguiente_ronda

def simular_torneo_jugador():
    print("Bienvenido al torneo de ninjas")

    if not arboles_ninja:
        print("No hay árboles de habilidades suficientes para un torneo.")
        return
    
    participantes = list(ninjas_pelea.keys())
    if len(participantes) < 2:
        print("No hay suficientes ninjas para iniciar el torneo.")
        return
     
    rondas=["Dieciseisavos", "Octavos", "Cuartos", "Semifinales", "Final"]


    for nombre_ronda in rondas:
        if len(participantes) ==1:
            break
        participantes = ronda(nombre_ronda, participantes, ninjas_pelea)

    if participantes:
        campeon=participantes[0]
        print(f"🥷🏆 \nEl campeón del torneo es: {campeon}")
        print(f"\n Habilidades del: {campeon}")
        mostrar_habilidades(ninjas_pelea[campeon])

def habilidades_con_ninja(nodo):
    if nodo is None:
        return 0
    return nodo.puntos + habilidades_con_ninja(nodo.izq) + habilidades_con_ninja(nodo.der)

def simulacion_de_combate():
    ninjas = leer_ninjas()
    if len(ninjas) < 2:
        print("No hay suficientes ninjas para simular un combate")
        return
    print("-"*10 +"Ninjas Disponibles" + "-"*10)
    for n,ninja in enumerate(ninjas, 1):
        print(f"{n}.{ninja['Nombre']} | Puntos: {ninja['Puntos']} | Estilo: {ninja['Estilo']} | Rango: {ninja['Rango']}")
    while True:
        try:
            entrada1 = int(input("Seleccione el primer ninja: ")) - 1
            entrada2 = int(input("Seleccione el segundo ninja: ")) - 1
            if entrada1 == entrada2 or entrada1 < 0 or entrada2 < 0 or entrada1 >= len(ninjas) or entrada2 >=len(ninjas):
                print("Error. Seleccion invalida ingrese ninjas validos")
                continue
            break
        except ValueError:
            print("Entrada invalida. Solo ingresar un numero")
            return
    primer_ninja_seleccionado = ninjas[entrada1]
    segundo_ninja_seleccionado = ninjas[entrada2]
    print(f"\n🤼 Combate: {primer_ninja_seleccionado['Nombre']}, VS {segundo_ninja_seleccionado['Nombre']}")
    arbol_ninja1 = arboles_ninja.get(primer_ninja_seleccionado['Nombre'])
    arbol_ninja2 = arboles_ninja.get(segundo_ninja_seleccionado['Nombre'])
    if not arbol_ninja1 or not arbol_ninja2:
        print("❎Error. Algun ninja no tiene designado un arbol de habilidades")
        return
    
    puntos_ninja1 = primer_ninja_seleccionado['Puntos'] + habilidades_con_ninja(arbol_ninja1) + random.randint(0,5)
    puntos_ninja2 = segundo_ninja_seleccionado['Puntos'] + habilidades_con_ninja(arbol_ninja2) + random.randint(0,5)

    print(f"{primer_ninja_seleccionado['Nombre']} ➡️ Total: {puntos_ninja1} puntos")
    print(f"{segundo_ninja_seleccionado['Nombre']} ➡️ Total: {puntos_ninja2} puntos")

    if puntos_ninja1 > puntos_ninja2:
        ganador = primer_ninja_seleccionado['Nombre']
    elif puntos_ninja2 > puntos_ninja1:
        ganador = segundo_ninja_seleccionado['Nombre']
    else:
        ganador = random.choice([primer_ninja_seleccionado['Nombre'], segundo_ninja_seleccionado['Nombre']])
    
    print(f"🏆 Resultado: {ganador} de la batalla")

    with open("combates.txt" ,"a" , encoding= "UTF-8") as f:
        f.write(f"{primer_ninja_seleccionado['Nombre']} VS {segundo_ninja_seleccionado['Nombre']} ➡️ Ganador: {ganador}\n")
        print("✅Resultado de los combates 1 vs 1 guardado correctamente.")

def ranking_consulta():
    if not os.path.exists("combates.txt"):
        print("No existen combates registrados")
        return
    victorias = {}
    with open("combates.txt","r",encoding="UTF-8") as f:
        for lineas in f:
            if "Ganador" in lineas:
                ganador = lineas.strip().split("Ganador:")[-1].strip()
                if ganador in victorias:
                    victorias[ganador] += 1
                else:
                    victorias[ganador] = 1 
    if not victorias:
        print("No existe ninguna victoria registrada actualmente")
        return
    rank = sorted(victorias.items(),key=lambda n:n[1],reverse=True)

    print("-"*10 +"📈Ranking Actualizado por Victorias"+"-"*10)
    print(f"{'Pos':<5}{'Ninja':<20}{'victorias'}")

    for i,(ninja,vic) in enumerate(rank,1):
        print(f"{i:<5}{ninja:<20}{vic}")

    with open("ranking.txt", "w",encoding="UTF-8") as f:
        for i, (ninja,vic) in enumerate(rank,1):
            f.write(f"{i}.{ninja} | {vic} victorias \n")
    print("\nRanking guardado exitosamente")
#Bucle 
while True:
    print("--------MENU PRINCIPAL---------")
    print("1. Rol Administrador")
    print("2. Rol Jugador")
    print("3. Salir")
    opcion_principal = int(input("Ingrese una opcion: "))
    if opcion_principal == 1:
        login_administrador()
        while True:
            menu_administrador()
            admin_opcion = int(input("Ingrese una opcion: "))
            if admin_opcion == 1:
                listas_de_ninjas = leer_ninjas()
                agregar_ninja(listas_de_ninjas)
                guardar_ninjas(listas_de_ninjas)
            elif admin_opcion == 2:
                ninjas_lista = leer_ninjas()
                listar_ninjas(ninjas_lista)
            elif admin_opcion == 3:
                ninjas_lista = leer_ninjas()
                buscar_ninja(ninjas_lista)
            elif admin_opcion == 4:
                ninjas_lista = leer_ninjas()
                ninja_a_actualizar(ninjas_lista)
                guardar_ninjas(ninjas_lista)
            elif admin_opcion == 5:
                ninjas_lista = leer_ninjas()
                eliminar_ninja(ninjas_lista)
                guardar_ninjas(ninjas_lista)
            elif admin_opcion == 6:
                crear_arbol_para_ninja()
                guardar_habilidades_ninja(habilidades)
            elif admin_opcion == 7:
                guardar_cambios_en_archivo_original()
            elif admin_opcion == 0:
                print("Saliendo del administrador.")
                break
            else: 
                print("Opcion ingresada no valida")
    elif opcion_principal == 2:
        usuario_actual = None
        while True:
            menu_jugador()
            opciones = int(input("Ingrese una opcion: "))
            if opciones == 1:
                agregar_usuario(usuarios)
            elif opciones == 2:
                lis = usuarios_registrados()
                usuario_actual = iniciar_sesion(lis)
            elif opciones == 3:
                ver_arbol_jugador()
            elif opciones == 4:
                simulacion_de_combate()
            elif opciones == 5:
                simular_torneo_jugador()
            elif opciones == 6:
                ranking_consulta()
            elif opciones == 0:
                print("Saliendo del juego.")
                break
            else:
                print("Opcion no valida")
    elif opcion_principal == 3:
        print("Gracias por usar el sistema. Saliendo.....")
        break
    else: 
        print("Opcion no valida. Intentelo nuevamente")