from collections import deque #Permite insertar y eliminar elementoos al principio/fin de una lista
from io import open #Abrir archivos compatibles con python
import os  #Verificacion de archivos
import re  #Validar patrones de texto
import random #Numeros aleatorios 
import datetime #Fecha y hora actual

archivo = "usuarios.txt"
ninjas_archivo = "ninjas.txt"
habilidades = "habilidades_ninja.txt"
progreso = "combates_usuario_email.txt"
usuarios = []
arboles_ninja = {}
ninjas = []
ninjas_pelea = {}

def inicializar_datos():
    global ninjas, ninjas_pelea, arboles_ninja  
    ninjas = leer_ninjas()
    cargar_habilidades_ninja(habilidades)
    ninjas_pelea = {ninja['Nombre']: arboles_ninja.get(ninja['Nombre']) for ninja in ninjas}

def actualizar_ninjas_pelea():
    global ninjas_pelea, ninjas, arboles_ninja
    ninjas = leer_ninjas()
    cargar_habilidades_ninja(habilidades)
    
    ninjas_pelea = {}
    for ninja in ninjas:
        if ninja['Nombre'] in arboles_ninja and arboles_ninja[ninja['Nombre']] is not None:
            if sumar_habilidades(arboles_ninja[ninja['Nombre']]) > 0:  # Verificar que tenga puntos
                ninjas_pelea[ninja['Nombre']] = arboles_ninja[ninja['Nombre']]
    
    if not ninjas_pelea:
        print("¡Advertencia! No hay ninjas con habilidades válidas")
    return len(ninjas_pelea) >= 2 


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

def guardar_habilidades_ninja(archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        for nombre, arbol in arboles_ninja.items():
            f.write(f"{nombre}\n")
            guardar_nodo(arbol, f)

def guardar_nodo(nodo, f, nivel=0):
    if nodo is None:
        f.write("None\n")
        return
    f.write(f"{nodo.nombre},{nodo.puntos}\n")
    guardar_nodo(nodo.izq, f, nivel+1)
    guardar_nodo(nodo.der, f, nivel+1)

def cargar_habilidades_ninja(archivo):
    if not os.path.exists(archivo):
        return
    with open(archivo, "r", encoding="utf-8") as f:
        lineas = deque(f.read().splitlines())
    while lineas:
        nombre = lineas.popleft()
        arboles_ninja[nombre] = reconstruir_arbol(lineas)

def reconstruir_arbol(lineas):
    if not lineas:
        return None
    linea = lineas.popleft()
    if linea == "None":
        return None
    nombre, puntos = linea.split(",")
    nodo = NodoHabilidad(nombre, int(puntos))
    nodo.izq = reconstruir_arbol(lineas)
    nodo.der = reconstruir_arbol(lineas)
    return nodo

def guardar_cambios_en_archivo_original():
    try:
        # Primero guardar los datos básicos de los ninjas
        guardar_ninjas(ninjas)
        
        # Luego guardar las habilidades en su archivo correspondiente
        with open(habilidades, "w", encoding="utf-8") as f:
            for nombre, arbol in arboles_ninja.items():
                f.write(f"{nombre}\n")
                # Guardar el árbol de forma estructurada
                guardar_nodo(arbol, f)
        
        print("✅ Todos los cambios guardados correctamente (ninjas y habilidades).")
    except Exception as e:
        print(f"❌ Error al guardar cambios: {e}")

#ROL JUGADOR
def menu_jugador():
    print("-----MENU JUGADOR-----")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("0. Salir")

def menu_opciones_jugador():
    print("-----MENU OPCIONES JUGADOR-----")
    print("1. Ver arbol de habilidades ninja")
    print("2. Simular combate 1 vs 1")
    print("3. Simular rondas del torneo")
    print("4. Consultar ranking")
    print("5. Guardar progreso")
    print("6- Ver historial de combates")
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

ninjas_pelea = {ninja['Nombre']: arboles_ninja.get(ninja['Nombre']) for ninja in ninjas}
#simular rondas del torneo
def ronda(nombre_ronda,participantes, ninjas_pelea, usuario_actual=None):
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
        
        ganador = ninja1 if puntos1 > puntos2 else ninja2 if puntos2 > puntos1 else random.choice([ninja1, ninja2])
        print(f"Ganador: {ganador} \n")
        siguiente_ronda.append(ganador)

        if usuario_actual:  # Guardar cada combate del torneo
            guardar_combate_usuario(
                usuario_actual,
                f"Combate (Torneo): {ninja1} vs {ninja2} | Ganador: {ganador}"
            )
    return siguiente_ronda

def simular_torneo_jugador(usuario_actual=None):
    actualizar_ninjas_pelea()
    
    if len(ninjas_pelea) < 2:
        print("❌ Necesitas mínimo 2 ninjas con habilidades para el torneo")
        return

    participantes = list(ninjas_pelea.keys())
    random.shuffle(participantes)  # Aleatoriza el orden
    
    print("\n🔥 COMIENZA EL TORNEO 🔥")
    
    # Sistema automático de rondas según participantes
    if len(participantes) >= 8:
        rondas = ["Octavos de final", "Cuartos de final", "Semifinal", "Final"]
    elif len(participantes) >= 4:
        rondas = ["Cuartos de final", "Semifinal", "Final"]
    else:
        rondas = ["Final"]

    for ronda in rondas:
        print(f"\n=== {ronda.upper()} ===")
        ganadores_ronda = []
        
        for i in range(0, len(participantes), 2):
            if i+1 >= len(participantes):  # Caso impar
                ganadores_ronda.append(participantes[i])
                continue
                
            ninja1 = participantes[i]
            ninja2 = participantes[i+1]
            
            # Simular combate
            puntos1 = sumar_habilidades(ninjas_pelea[ninja1])
            puntos2 = sumar_habilidades(ninjas_pelea[ninja2])
            
            print(f"\n• {ninja1} vs {ninja2}")
            print(f"  {ninja1}: {puntos1} pts | {ninja2}: {puntos2} pts")
            
            ganador = ninja1 if puntos1 > puntos2 else ninja2 if puntos2 > puntos1 else random.choice([ninja1, ninja2])
            print(f"  ⚡GANADOR: {ganador}")
            ganadores_ronda.append(ganador)
            
            if usuario_actual:
                guardar_combate_usuario(usuario_actual, f"Torneo ({ronda}): {ninja1} vs {ninja2} | Ganador: {ganador}")
        
        participantes = ganadores_ronda
    
    print(f"\n🎉 CAMPEÓN DEL TORNEO: {participantes[0]} 🎉")
    mostrar_habilidades(ninjas_pelea[participantes[0]])

def habilidades_con_ninja(nodo):
    if nodo is None:
        return 0
    return nodo.puntos + habilidades_con_ninja(nodo.izq) + habilidades_con_ninja(nodo.der)

def simulacion_de_combate(usuario_actual=None):
    if not actualizar_ninjas_pelea():
        print("❌ No hay ninjas con habilidades asignadas")
        return
    
    actualizar_ninjas_pelea()  
    
    print("\n=== NINJAS DISPONIBLES ===")
    ninjas_con_habilidades = list(ninjas_pelea.keys())
    for idx, nombre in enumerate(ninjas_con_habilidades, 1):
        print(f"{idx}. {nombre}")

    try:
        # Selección de ninjas
        eleccion1 = int(input("\nSelecciona al primer ninja: ")) - 1
        eleccion2 = int(input("Selecciona al segundo ninja: ")) - 1
        
        if eleccion1 == eleccion2:
            print("⚠️ Debes seleccionar ninjas diferentes")
            return
            
        nombre_ninja1 = ninjas_con_habilidades[eleccion1]
        nombre_ninja2 = ninjas_con_habilidades[eleccion2]
        
        # Obtener datos completos
        todos_ninjas = leer_ninjas()
        ninja1 = next(n for n in todos_ninjas if n['Nombre'] == nombre_ninja1)
        ninja2 = next(n for n in todos_ninjas if n['Nombre'] == nombre_ninja2)
        
        # Calcular puntos
        puntos1 = ninja1['Puntos'] + sumar_habilidades(ninjas_pelea[nombre_ninja1])
        puntos2 = ninja2['Puntos'] + sumar_habilidades(ninjas_pelea[nombre_ninja2])
        
        # Resultado
        print(f"\n⚔️ COMBATE: {nombre_ninja1} vs {nombre_ninja2}")
        print(f"• {nombre_ninja1}: {puntos1} puntos")
        print(f"• {nombre_ninja2}: {puntos2} puntos")
        
        ganador = nombre_ninja1 if puntos1 > puntos2 else nombre_ninja2 if puntos2 > puntos1 else random.choice([nombre_ninja1, nombre_ninja2])
        print(f"\n🏆 GANADOR: {ganador}!")
        
        # Guardar registro
        with open("combates.txt", "a", encoding="utf-8") as f:
            f.write(f"{nombre_ninja1} VS {nombre_ninja2} | Ganador: {ganador}\n")
            
        if usuario_actual:
            guardar_combate_usuario(usuario_actual, f"Combate: {nombre_ninja1} vs {nombre_ninja2} | Ganador: {ganador}")
            
    except (ValueError, IndexError):
        print("❌ Error: Selección inválida")

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

def guardar_combate_usuario(email, resultado):
    # Reemplazar caracteres no válidos en el nombre del archivo
    nombre_archivo = f"combates_usuario_{email.replace('@', '_').replace('.', '_')}.txt"
    fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open(nombre_archivo, "a", encoding="utf-8") as f:
            f.write(f"{fecha_actual} - {resultado}\n")
    except Exception as e:
        print(f"Error al guardar combate personal: {e}")

def mostrar_historial_usuario(email):
    nombre_archivo = f"combates_usuario_{email.replace('@', '_').replace('.', '_')}.txt"
    if not os.path.exists(nombre_archivo):
        print("No tienes combates registrados aún.")
        return
    
    print(f"\n📜 Historial de combates de {email}:")
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            print(linea.strip())

#Bucle 
inicializar_datos()
while True:
    print("--------MENU PRINCIPAL---------")
    print("1. Rol Administrador")
    print("2. Rol Jugador")
    print("0. Salir")
    try:
        opcion_principal = int(input("Ingrese una opcion: "))
        if opcion_principal == 1:
            login_administrador()
            while True:
                menu_administrador()
                try:
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
                except ValueError:
                    print("Entrada no valida. Ingrese un numero")
        elif opcion_principal == 2:
            usuario_actual = None
            inicializar_datos()
            while True:
                menu_jugador()
                try:
                    opciones = int(input("Ingrese una opcion: "))
                    if opciones == 1:
                        agregar_usuario(usuarios)
                    elif opciones == 2:
                        lis = usuarios_registrados()
                        usuario_actual = iniciar_sesion(lis)
                        if usuario_actual:
                            actualizar_ninjas_pelea()  # Actualiza los ninjas al iniciar sesión
                        while True:
                            menu_opciones_jugador()
                            opcion_usuario = int(input("Ingrese una opcion: "))
                            if opcion_usuario == 1:
                                ver_arbol_jugador()
                            elif opcion_usuario == 2:
                                actualizar_ninjas_pelea() 
                                simulacion_de_combate(usuario_actual)
                            elif opcion_usuario == 3:
                                actualizar_ninjas_pelea()
                                simular_torneo_jugador()
                            elif opcion_usuario == 4:
                                ranking_consulta()
                            elif opcion_usuario == 5:
                                guardar_usuario(archivo, usuarios)
                                print("Progreso guardado exitosamente")
                            elif opcion_usuario == 6:
                                mostrar_historial_usuario(usuario_actual)
                            elif opcion_usuario == 0:
                                print("Saliendo del menu de opciones.")
                                break
                            else:
                                print("Opcion no valida. Intente nuevamente")
                    elif opciones == 0:
                        print("Saliendo del rol jugador.")
                        break
                    else:
                        print("Opcion no valida. Intente nuevamente")
                except ValueError:
                    print("Entrada no valida. Ingrese un numero")
                
        elif opcion_principal == 0:
            print("Gracias por usar el sistema. Saliendo.")
            break
        else: 
            print("Opcion no valida. Intentelo nuevamente")
    except ValueError:
        print("Entrada no valida. Ingrese un numero")