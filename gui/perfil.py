import tkinter as tk
from tkinter import ttk, messagebox
from database.mysql_connection import obtener_progreso, conectar_mysql
from collections import defaultdict

# Función para mostrar el perfil de un jugador
def mostrar_perfil_jugador(nombre_jugador):
    def obtener_estadisticas_detalladas():
        conexion = conectar_mysql()
        cursor = conexion.cursor()
        
        # Obtener el progreso general del jugador
        cursor.execute("SELECT categoria, COUNT(*) FROM Adivinanzas GROUP BY categoria")
        adivinanzas_por_categoria = dict(cursor.fetchall())
        total_adivinanzas = sum(adivinanzas_por_categoria.values())
        
        # Obtener el progreso del jugador
        respondidas_por_categoria = defaultdict(int)
        puntos_por_categoria = defaultdict(int)
        intentos_por_categoria = defaultdict(int)
        
        # Obtener el progreso general del jugador
        for progreso in progreso_general:
            categoria = progreso['categoria']
            respondidas_por_categoria[categoria] = len(progreso['adivinanzas_respondidas'])
            puntos_por_categoria[categoria] = progreso['puntos']
        
        cursor.close()
        conexion.close()
        
        return total_adivinanzas, adivinanzas_por_categoria, respondidas_por_categoria, puntos_por_categoria, intentos_por_categoria
    
    # Función para actualizar las estadísticas en la ventana
    def actualizar_estadisticas():
        for widget in frame_estadisticas.winfo_children():
            widget.destroy()

        total_adivinanzas, adivinanzas_por_categoria, respondidas_por_categoria, puntos_por_categoria, intentos_por_categoria = obtener_estadisticas_detalladas()
        
        mostrar_estadisticas_generales(total_adivinanzas, respondidas_por_categoria, puntos_por_categoria, intentos_por_categoria)
        mostrar_estadisticas_por_categoria(adivinanzas_por_categoria, respondidas_por_categoria, puntos_por_categoria, intentos_por_categoria)
        mostrar_categoria_favorita(respondidas_por_categoria)
        mostrar_retroalimentacion(total_adivinanzas, respondidas_por_categoria, puntos_por_categoria, intentos_por_categoria)
    
    # Función para mostrar las estadísticas generales del jugador
    def mostrar_estadisticas_generales(total_adivinanzas, respondidas_por_categoria, puntos_por_categoria, intentos_por_categoria):
        total_puntos = sum(puntos_por_categoria.values())
        total_intentos = sum(intentos_por_categoria.values())
        total_respondidas = sum(respondidas_por_categoria.values())
        
        indice_eficiencia = (total_puntos / (total_respondidas * 2)) * 100 if total_respondidas > 0 else 0

        # Estadísticas generales
        estadisticas = [
            f"Puntos totales: {total_puntos}",
            f"Adivinanzas respondidas: {total_respondidas} de {total_adivinanzas}",
            f"Progreso general: {(total_respondidas / total_adivinanzas * 100):.1f}%",
            f"Índice de eficiencia: {indice_eficiencia:.1f}%"
        ]

        # Mostrar las estadísticas generales
        tk.Label(frame_estadisticas, text="Estadísticas generales", font=("Arial", 14, "bold")).pack(anchor='w', pady=(0, 5))
        for estadistica in estadisticas:
            tk.Label(frame_estadisticas, text=estadistica, font=("Arial", 12)).pack(anchor='w')

    # Función para mostrar las estadísticas por categoría
    def mostrar_estadisticas_por_categoria(adivinanzas_por_categoria, respondidas_por_categoria, puntos_por_categoria, intentos_por_categoria):
        tk.Label(frame_estadisticas, text="\nEstadísticas por categoría", font=("Arial", 14, "bold")).pack(anchor='w', pady=(10, 5))
        for categoria, total in adivinanzas_por_categoria.items():
            respondidas = respondidas_por_categoria[categoria]
            puntos = puntos_por_categoria[categoria]
            porcentaje = (respondidas / total) * 100
            indice_eficiencia = (puntos / (respondidas * 2)) * 100 if respondidas > 0 else 0
            estadistica = f"{categoria}: {respondidas} de {total} ({porcentaje:.1f}%) - Puntos: {puntos}, Eficiencia: {indice_eficiencia:.1f}%"
            tk.Label(frame_estadisticas, text=estadistica, font=("Arial", 12)).pack(anchor='w')
            
    # Función para mostrar la categoría favorita del jugador
    def mostrar_categoria_favorita(respondidas_por_categoria):
        if respondidas_por_categoria:
            categoria_favorita = max(respondidas_por_categoria, key=respondidas_por_categoria.get)
            tk.Label(frame_estadisticas, text=f"\nCategoría favorita: {categoria_favorita}", font=("Arial", 12, "bold")).pack(anchor='w', pady=(10, 0))

    # Función para mostrar la retroalimentación del jugador
    def mostrar_retroalimentacion(total_adivinanzas, respondidas_por_categoria, puntos_por_categoria, intentos_por_categoria):
        total_respondidas = sum(respondidas_por_categoria.values())
        total_puntos = sum(puntos_por_categoria.values())
        
        indice_eficiencia = (total_puntos / (total_respondidas * 2)) * 100 if total_respondidas > 0 else 0

        # Retroalimentación
        if indice_eficiencia < 10:
            retroalimentacion = "Estás empezando tu viaje en el mundo de las adivinanzas. ¡Cada intento es una oportunidad para aprender! Sigue practicando y verás cómo mejoras poco a poco."
        elif indice_eficiencia < 20:
            retroalimentacion = "Vas progresando. Intenta leer las adivinanzas con más atención y piensa en todas las posibles respuestas antes de contestar. ¡Tú puedes mejorar!"
        elif indice_eficiencia < 30:
            retroalimentacion = "Estás mejorando tu eficiencia. Trata de relacionar las pistas de las adivinanzas con tus conocimientos. Con práctica, lograrás responder más rápido y preciso."
        elif indice_eficiencia < 40:
            retroalimentacion = "Buen trabajo, estás en el camino correcto. Intenta concentrarte más en las categorías que te resultan más difíciles para equilibrar tu rendimiento."
        elif indice_eficiencia < 50:
            retroalimentacion = "Estás alcanzando un buen nivel. Desafíate a ti mismo intentando responder más adivinanzas en el primer intento. ¡Sigue así!"
        elif indice_eficiencia < 60:
            retroalimentacion = "Tu eficiencia es notable. Estás demostrando una buena comprensión de las adivinanzas. Sigue practicando para mejorar aún más."
        elif indice_eficiencia < 70:
            retroalimentacion = "¡Impresionante progreso! Tu habilidad para resolver adivinanzas está creciendo. Intenta aumentar tu velocidad de respuesta sin perder precisión."
        elif indice_eficiencia < 80:
            retroalimentacion = "Excelente rendimiento. Estás mostrando una gran habilidad. Enfócate en las categorías más desafiantes para llevar tu juego al siguiente nivel."
        elif indice_eficiencia < 90:
            retroalimentacion = "¡Fantástico! Eres muy hábil resolviendo adivinanzas. Prueba a desafiarte con adivinanzas más complejas para seguir mejorando."
        else:
            retroalimentacion = f"¡Increíble! Eres un maestro de las adivinanzas con un índice de eficiencia del {indice_eficiencia:.1f}%. ¿Puedes mantener este nivel excepcional en todas las categorías?"

        tk.Label(frame_estadisticas, text="\nRetroalimentación:", font=("Arial", 14, "bold")).pack(anchor='w', pady=(10, 5))
        tk.Label(frame_estadisticas, text=retroalimentacion, font=("Arial", 12), wraplength=350, justify='left').pack(anchor='w')

    # Configuración de la ventana principal
    ventana_perfil = tk.Toplevel()
    ventana_perfil.title(f"Perfil de {nombre_jugador}")
    
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_perfil.winfo_screenwidth()
    alto_pantalla = ventana_perfil.winfo_screenheight()

    # Obtener las dimensiones de la ventana
    ancho_ventana = 500
    alto_ventana = 650

    # Calcular la posición x, y para el centro de la pantalla
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)

    # Establecer la geometría de la ventana
    ventana_perfil.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

    # Hacer que la ventana no sea redimensionable
    ventana_perfil.resizable(False, False)

    frame_principal = tk.Frame(ventana_perfil)
    frame_principal.pack(expand=True, fill='both', padx=20, pady=20)

    etiqueta_nombre = tk.Label(frame_principal, text=f"Perfil de {nombre_jugador}", font=("Arial", 18, "bold"))
    etiqueta_nombre.pack(pady=(0, 20))

    frame_estadisticas = tk.Frame(frame_principal)
    frame_estadisticas.pack(fill='both', expand=True)

    frame_botones = tk.Frame(frame_principal)
    frame_botones.pack(pady=20)

    boton_actualizar = tk.Button(frame_botones, text="Actualizar estadísticas", command=actualizar_estadisticas, font=("Arial", 12))
    boton_actualizar.pack(side=tk.LEFT, padx=5)

    boton_cerrar = tk.Button(frame_botones, text="Cerrar", command=ventana_perfil.destroy, font=("Arial", 12))
    boton_cerrar.pack(side=tk.LEFT, padx=5)

    # Obtener el progreso general y mostrar las estadísticas iniciales
    progreso_general = obtener_progreso(nombre_jugador)
    actualizar_estadisticas()

    ventana_perfil.mainloop()
