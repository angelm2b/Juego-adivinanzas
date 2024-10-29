import tkinter as tk
from tkinter import ttk, messagebox, Menu
from database.mysql_connection import conectar_mysql
from gui.adivinanza import mostrar_pantalla_adivinanza
from gui.perfil import mostrar_perfil_jugador

# Función para mostrar la pantalla de selección de categoría
def mostrar_pantalla_seleccion_categoria(nombre_jugador, progreso=None):
    def seleccionar_categoria():
        categoria = combo_categorias.get()
        if categoria:
            ventana_seleccion.destroy()
            mostrar_pantalla_adivinanza(categoria, nombre_jugador, mostrar_pantalla_seleccion_categoria, progreso)
        else:
            messagebox.showerror("Error", "Por favor, selecciona una categoría antes de continuar.")

    # Función para volver al inicio
    def volver_inicio():
        ventana_seleccion.destroy()
        from gui.inicio import mostrar_pantalla_inicio
        mostrar_pantalla_inicio()
        
    # Función para ver el perfil del jugador
    def ver_perfil():
        mostrar_perfil_jugador(nombre_jugador)

    # Función para obtener las categorías de la base de datos
    def obtener_categorias():
        conexion = conectar_mysql()
        cursor = conexion.cursor()
        cursor.execute("SELECT DISTINCT categoria FROM Adivinanzas")
        categorias = [categoria[0] for categoria in cursor.fetchall()]
        cursor.close()
        conexion.close()
        return categorias

    # Crear la ventana de selección de categoría
    ventana_seleccion = tk.Tk()
    ventana_seleccion.title("Selección de Categoría")
    
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_seleccion.winfo_screenwidth()
    alto_pantalla = ventana_seleccion.winfo_screenheight()

    # Obtener las dimensiones de la ventana
    ancho_ventana = 400
    alto_ventana = 350

    # Calcular la posición x, y para el centro de la pantalla
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)

    # Establecer la geometría de la ventana
    ventana_seleccion.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

    # Hacer que la ventana no sea redimensionable
    ventana_seleccion.resizable(False, False)

    # Barra de menú
    barra_menu = Menu(ventana_seleccion)
    ventana_seleccion.config(menu=barra_menu)

    # Menú de opciones
    menu_opciones = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Opciones", menu=menu_opciones)
    menu_opciones.add_command(label="Ver Perfil", command=ver_perfil)
    menu_opciones.add_command(label="Volver al Inicio", command=volver_inicio)

    # Frame principal
    frame_principal = tk.Frame(ventana_seleccion)
    frame_principal.pack(expand=True, fill='both', padx=20, pady=20)

    etiqueta_bienvenida = tk.Label(frame_principal, text=f"Bienvenido, {nombre_jugador}", font=("Arial", 18, "bold"))
    etiqueta_bienvenida.pack(pady=20)

    etiqueta_seleccion = tk.Label(frame_principal, text="Selecciona una categoría:", font=("Arial", 12))
    etiqueta_seleccion.pack()

    # Obtener las categorías de la base de datos
    categorias = obtener_categorias()
    combo_categorias = ttk.Combobox(frame_principal, values=categorias, font=("Arial", 12), width=30)
    combo_categorias.pack(pady=10)

    boton_jugar = tk.Button(frame_principal, text="Jugar", command=seleccionar_categoria, font=("Arial", 12))
    boton_jugar.pack(pady=5)

    boton_perfil = tk.Button(frame_principal, text="Ver Perfil", command=ver_perfil, font=("Arial", 12))
    boton_perfil.pack(pady=5)

    boton_volver = tk.Button(frame_principal, text="Volver al Inicio", command=volver_inicio, font=("Arial", 12))
    boton_volver.pack(pady=5)

    ventana_seleccion.mainloop()
