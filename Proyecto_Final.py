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
def crear_arbol_personalizado(nombre_ninja):
    print(f"\n--- Asignar habilidades a {nombre_ninja} ---")
    habilidades = []
    for i in range(1, 5):
        habilidad = input(f"Ingrese habilidad {i}: ").strip()
        habilidades.append(habilidad)

    raiz = NodoHabilidad(habilidades[0], random.randint(6, 10))
    raiz.izq = NodoHabilidad(habilidades[1], random.randint(6, 10))
    raiz.der = NodoHabilidad(habilidades[2], random.randint(6, 10))
    raiz.izq.izq = NodoHabilidad(habilidades[3], random.randint(6, 10))

    return raiz
def mostrar_habilidades(nodo, nivel=0):
    if nodo:
        print("  " * nivel + f"{nodo.nombre}")
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

def crer_arbol_para_ninja():
    nombre = input("Nombre del ninja para asignar habilidades: ").strip()
    if nombre == "":
        print("Nombre inválido.")
        return
    arbol = crear_arbol_personalizado(nombre)
    arboles_ninja[nombre] = arbol
    print(f"Arbol de habilidades creado y guardado para {nombre}.")

#ROL JUGADOR
def menu_jugador():
    print("-----MENU JUGADOR-----")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Ver arbol de habilidades ninja")
    print("4. Simular combate")
    print("5. Salir")

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
                #falta agregar opciones 4 y 5
            elif admin_opcion == 6:
                crer_arbol_para_ninja()
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
