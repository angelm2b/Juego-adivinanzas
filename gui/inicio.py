import tkinter as tk
from tkinter import messagebox, Menu
import sys
from gui.seleccion_categoria import mostrar_pantalla_seleccion_categoria
from gui.perfil import mostrar_perfil_jugador
from database.mysql_connection import obtener_progreso
from gui.acerca_de import mostrar_acerca_de

# Función principal para mostrar la pantalla de inicio
def mostrar_pantalla_inicio():
    # Función para iniciar el juego
    def iniciar_juego():
        nombre = entrada_nombre.get().strip()
        if nombre:
            ventana_inicio.destroy()
            progreso = obtener_progreso(nombre)
            mostrar_pantalla_seleccion_categoria(nombre, progreso)
        else:
            messagebox.showerror("Error", "Por favor, ingresa tu nombre.")

    # Función para ver el perfil del jugador
    def ver_perfil():
        nombre = entrada_nombre.get().strip()
        if nombre:
            mostrar_perfil_jugador(nombre)
        else:
            messagebox.showerror("Error", "Por favor, ingresa tu nombre para ver el perfil.")

    # Función para salir del programa
    def salir_programa():
        if messagebox.askokcancel("Salir", "¿Estás seguro que quieres salir del juego?"):
            ventana_inicio.quit()
            ventana_inicio.destroy()
            sys.exit()

    # Crear la ventana de inicio
    ventana_inicio = tk.Tk()
    ventana_inicio.title("Bienvenido a Adivinanzas")
    
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_inicio.winfo_screenwidth()
    alto_pantalla = ventana_inicio.winfo_screenheight()

    # Obtener las dimensiones de la ventana
    ancho_ventana = 400
    alto_ventana = 370

    # Calcular la posición x, y para el centro de la pantalla
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)

    # Establecer la geometría de la ventana
    ventana_inicio.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

    # Hacer que la ventana no sea redimensionable
    ventana_inicio.resizable(False, False)

    # Barra de menú
    barra_menu = Menu(ventana_inicio)
    ventana_inicio.config(menu=barra_menu)

    menu_archivo = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
    menu_archivo.add_command(label="Salir", command=salir_programa)

    menu_ayuda = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Acerca de", command=mostrar_acerca_de)

    frame_principal = tk.Frame(ventana_inicio)
    frame_principal.pack(expand=True, fill='both', padx=20, pady=20)

    etiqueta_bienvenida = tk.Label(frame_principal, text="Bienvenido a Adivinanzas", font=("Arial", 18, "bold"))
    etiqueta_bienvenida.pack(pady=20)

    etiqueta_nombre = tk.Label(frame_principal, text="Ingresa tu nombre:", font=("Arial", 12))
    etiqueta_nombre.pack()

    entrada_nombre = tk.Entry(frame_principal, font=("Arial", 12), width=30)
    entrada_nombre.pack(pady=10)

    boton_iniciar = tk.Button(frame_principal, text="Iniciar Juego", command=iniciar_juego, font=("Arial", 12))
    boton_iniciar.pack(pady=5)

    boton_perfil = tk.Button(frame_principal, text="Ver Perfil", command=ver_perfil, font=("Arial", 12))
    boton_perfil.pack(pady=5)

    boton_salir = tk.Button(frame_principal, text="Salir", command=salir_programa, font=("Arial", 12))
    boton_salir.pack(pady=5)
    
    boton_acerca_de = tk.Button(frame_principal, text="Acerca de", command=mostrar_acerca_de, font=("Arial", 12))
    boton_acerca_de.pack(pady=25)

    ventana_inicio.protocol("WM_DELETE_WINDOW", salir_programa)
    ventana_inicio.mainloop()

    mostrar_pantalla_inicio()
