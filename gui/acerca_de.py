import tkinter as tk
from tkinter import ttk
import webbrowser
from database.mysql_connection import conectar_mysql

def abrir_enlace(url):
    webbrowser.open_new(url)

def mostrar_acerca_de():
    # Crear una nueva ventana
    ventana_acerca_de = tk.Toplevel()
    ventana_acerca_de.title("Acerca de Adivinanzas")
    
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_acerca_de.winfo_screenwidth()
    alto_pantalla = ventana_acerca_de.winfo_screenheight()

    # Obtener las dimensiones de la ventana
    ancho_ventana = 600
    alto_ventana = 700

    # Calcular la posición x, y para el centro de la pantalla
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)

    # Establecer la geometría de la ventana
    ventana_acerca_de.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

    # Hacer que la ventana no sea redimensionable
    ventana_acerca_de.resizable(False, False)
    
    # Crear un canvas con barra de desplazamiento
    canvas = tk.Canvas(ventana_acerca_de)
    scrollbar = ttk.Scrollbar(ventana_acerca_de, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda _: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((ancho_ventana // 2, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Información del juego
    ttk.Label(scrollable_frame, text="Juego de Adivinanzas", font=("Arial", 23, "bold")).pack(pady=25)
    ttk.Label(scrollable_frame, text="Versión 1.0", font=("Arial", 17)).pack()
    ttk.Label(scrollable_frame, text="Desarrollado por:", font=("Arial", 17, "bold")).pack(pady=(25, 5))
    enlace = ttk.Label(scrollable_frame, text="Angelm2b", font=("Arial", 17,"underline"))
    enlace.pack()
    enlace.bind("<Button-1>", lambda e: abrir_enlace("https://angelm2b.onrender.com/"))
    
    # Descripción del juego
    descripcion = "Un emocionante juego de adivinanzas para poner a prueba tu ingenio y conocimientos generales."
    ttk.Label(scrollable_frame, text=descripcion, font=("Arial", 15), justify="center", wraplength=ancho_ventana-50).pack(pady=(25, 0))
    
    # Reglas del juego
    ttk.Label(scrollable_frame, text="Reglas del Juego", font=("Arial", 19, "bold")).pack(pady=(25, 15))
    reglas = [
        "1. Selecciona una categoría de adivinanzas.",
        "2. Lee cuidadosamente cada adivinanza presentada.",
        "3. Tienes 2 intentos para adivinar la respuesta correcta.",
        "4. Escribe tu respuesta en el campo de texto proporcionado.",
        "5. Haz clic en 'Verificar' para comprobar tu respuesta.",
        "6. Ganas 2 puntos por respuesta correcta en el primer intento, 1 punto en el segundo.",
        "7. Tu progreso se guarda automáticamente.",
        "8. Puedes ver tu perfil y estadísticas en cualquier momento.",
        "9. Completa todas las adivinanzas disponibles para mejorar tu puntuación."
    ]
    for regla in reglas:
        ttk.Label(scrollable_frame, text=regla, font=("Arial", 13), justify="left", wraplength=ancho_ventana-50).pack(pady=5, anchor="w")

    # Estadísticas del juego
    ttk.Label(scrollable_frame, text="Estadísticas del Juego", font=("Arial", 19, "bold")).pack(pady=(30, 15))
    
    # Obtener estadísticas de la base de datos
    conexion = conectar_mysql()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM Adivinanzas")
    total_adivinanzas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT categoria) FROM Adivinanzas")
    total_categorias = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Progreso")
    total_jugadores = cursor.fetchone()[0]
    
    conexion.close()

    estadisticas = [
        f"Total de adivinanzas: {total_adivinanzas}",
        f"Categorías disponibles: {total_categorias}",
        f"Jugadores registrados: {total_jugadores}"
    ]
    for stat in estadisticas:
        ttk.Label(scrollable_frame, text=stat, font=("Arial", 13), justify="left").pack(pady=5, anchor="w")

    # Botón para cerrar la ventana
    ttk.Button(scrollable_frame, text="Cerrar", command=ventana_acerca_de.destroy, style='TButton').pack(pady=30)
    
    # Estilo para el botón
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 15))    

    # Configurar el canvas y la barra de desplazamiento
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Hacer que la ventana sea modal
    ventana_acerca_de.transient(ventana_acerca_de.master)
    ventana_acerca_de.grab_set()
    ventana_acerca_de.wait_window()

    mostrar_acerca_de.mainloop()