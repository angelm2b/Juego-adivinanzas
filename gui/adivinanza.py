import tkinter as tk
from tkinter import messagebox
from database.mysql_connection import conectar_mysql, obtener_progreso, guardar_progreso
from utils.grafo_adivinanzas import GrafoAdivinanzas
from gui.perfil import mostrar_perfil_jugador

# Función principal para mostrar la pantalla de adivinanza
def mostrar_pantalla_adivinanza(categoria, nombre_jugador, callback_seleccion_categoria, progreso=None):
    # Función para verificar la respuesta del jugador
    def verificar_respuesta():
        nonlocal intentos, respuestas_correctas, intentos_totales, adivinanza_actual, puntos_sesion

        respuesta = entrada_respuesta.get().strip().lower()
        # Validar que la respuesta no esté en blanco
        if not respuesta:
            messagebox.showerror("Error", "La respuesta no puede estar en blanco. Por favor, ingrese una respuesta.")
            return 
        
        # Comprobación de respuesta correcta
        if respuesta == adivinanza_actual['respuesta'].lower():
            # Asignación de puntos según el número de intentos
            if intentos == 0:
                puntos_sesion += 2  # 2 puntos en el primer intento
            else:
                puntos_sesion += 1  # 1 punto en el segundo intento
            respuestas_correctas += puntos_sesion  # Actualizar respuestas_correctas
            messagebox.showinfo("Correcto", f"¡Respuesta correcta! Has ganado {2 if intentos == 0 else 1} punto(s).")
            grafo_adivinanzas.marcar_como_respondida(adivinanza_actual['id'])
            guardar_progreso_usuario()
            siguiente_pregunta()
        else:
            # Manejo de respuesta incorrecta
            intentos += 1
            intentos_totales += 1
            if intentos < 2:
                messagebox.showwarning("Incorrecto", "Respuesta incorrecta. Te queda 1 intento.")
                entrada_respuesta.delete(0, tk.END)
            else:
                messagebox.showwarning("Incorrecto", f"Respuesta incorrecta. La respuesta correcta era: {adivinanza_actual['respuesta']}")
                grafo_adivinanzas.marcar_como_respondida(adivinanza_actual['id'])
                guardar_progreso_usuario()
                siguiente_pregunta()
                
    # Función para pasar a la siguiente pregunta
    def siguiente_pregunta():
        nonlocal intentos, adivinanza_actual, preguntas_mostradas

        intentos = 0
        siguiente_id = grafo_adivinanzas.obtener_siguiente_adivinanza()
        
        if siguiente_id is not None and preguntas_mostradas < 3:
            adivinanza_actual = grafo_adivinanzas.obtener_adivinanza(siguiente_id)
            preguntas_mostradas += 1
            actualizar_pantalla_adivinanza()
        else:
            finalizar_juego()
            
    # Función para obtener adivinanzas de la base de datos
    def obtener_adivinanzas(categoria):
        conexion = conectar_mysql()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Adivinanzas WHERE categoria = %s", (categoria,))
        todas_adivinanzas = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        grafo = GrafoAdivinanzas()
        for adivinanza in todas_adivinanzas:
            grafo.agregar_adivinanza(adivinanza['id'], adivinanza)
        
        return grafo

    # Función para actualizar la pantalla con la adivinanza actual
    def actualizar_pantalla_adivinanza():
        etiqueta_adivinanza.config(text=adivinanza_actual['texto'])
        entrada_respuesta.delete(0, tk.END)
        etiqueta_progreso.config(text=f"Pregunta {preguntas_mostradas} de 3")

    # Función para guardar el progreso del usuario
    def guardar_progreso_usuario():
        nonlocal puntos_sesion
        progreso_actual = obtener_progreso(nombre_jugador, categoria) or {"puntos": 0, "intentos": 0, "adivinanzas_respondidas": []}
        progreso_actual["puntos"] += puntos_sesion
        progreso_actual["intentos"] = intentos_totales
        progreso_actual["adivinanzas_respondidas"] = list(set(progreso_actual["adivinanzas_respondidas"] + list(grafo_adivinanzas.adivinanzas_respondidas)))
        guardar_progreso(nombre_jugador, categoria, progreso_actual)
        puntos_sesion = 0  # Reiniciar los puntos de la sesión después de guardar

    # Función para finalizar el juego
    def finalizar_juego():
        ventana_adivinanza.destroy()
        if grafo_adivinanzas.todas_respondidas():
            messagebox.showinfo("Fin del juego", "¡Has respondido todas las adivinanzas disponibles en esta categoría!")
        else:
            messagebox.showinfo("Fin del juego", f"Has obtenido {respuestas_correctas} puntos en 3 preguntas.")
        callback_seleccion_categoria(nombre_jugador)

    # Función para volver a la selección de categoría
    def volver_seleccion():
        ventana_adivinanza.destroy()
        callback_seleccion_categoria(nombre_jugador)

    # Función para ver el perfil del jugador
    def ver_perfil():
        mostrar_perfil_jugador(nombre_jugador)

    # Configuración de la ventana principal
    ventana_adivinanza = tk.Tk()
    ventana_adivinanza.title(f"Adivinanza - {categoria}")
    
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_adivinanza.winfo_screenwidth()
    alto_pantalla = ventana_adivinanza.winfo_screenheight()

    # Obtener las dimensiones de la ventana
    ancho_ventana = 500
    alto_ventana = 400

    # Calcular la posición x, y para el centro de la pantalla
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)

    # Establecer la geometría de la ventana
    ventana_adivinanza.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

    # Hacer que la ventana no sea redimensionable
    ventana_adivinanza.resizable(False, False)

    grafo_adivinanzas = obtener_adivinanzas(categoria)
    
    # Cargar progreso del usuario
    progreso_usuario = obtener_progreso(nombre_jugador, categoria)
    if progreso_usuario:
        intentos_totales = progreso_usuario["intentos"]
        for adivinanza_id in progreso_usuario["adivinanzas_respondidas"]:
            if adivinanza_id in grafo_adivinanzas.grafo.nodes():
                grafo_adivinanzas.marcar_como_respondida(adivinanza_id)
    else:
        intentos_totales = 0

    # Inicialización de variables de juego
    adivinanza_actual = None
    intentos = 0
    puntos_sesion = 0  # Puntos ganados en la sesión actual
    preguntas_mostradas = 0
    respuestas_correctas = 0

    # Comprobación si todas las adivinanzas han sido respondidas
    if grafo_adivinanzas.todas_respondidas():
        messagebox.showinfo("Categoría completada", "Ya has respondido todas las adivinanzas de esta categoría.")
        ventana_adivinanza.destroy()
        callback_seleccion_categoria(nombre_jugador)
        return

    # Creación de elementos de la interfaz gráfica
    etiqueta_categoria = tk.Label(ventana_adivinanza, text=f"Categoría: {categoria}", font=("Arial", 14))
    etiqueta_categoria.pack(pady=10)

    etiqueta_adivinanza = tk.Label(ventana_adivinanza, text="", font=("Arial", 12), wraplength=400)
    etiqueta_adivinanza.pack(pady=20)

    entrada_respuesta = tk.Entry(ventana_adivinanza, font=("Arial", 12))
    entrada_respuesta.pack(pady=10)

    boton_verificar = tk.Button(ventana_adivinanza, text="Verificar", command=verificar_respuesta, font=("Arial", 12))
    boton_verificar.pack(pady=10)

    etiqueta_progreso = tk.Label(ventana_adivinanza, text="", font=("Arial", 12))
    etiqueta_progreso.pack(pady=10)

    boton_perfil = tk.Button(ventana_adivinanza, text="Ver Perfil", command=ver_perfil, font=("Arial", 12))
    boton_perfil.pack(pady=5)

    boton_volver = tk.Button(ventana_adivinanza, text="Volver a Selección", command=volver_seleccion, font=("Arial", 12))
    boton_volver.pack(pady=5)

    siguiente_pregunta()

    ventana_adivinanza.mainloop()