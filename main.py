from database.mysql_connection import inicializar_db
from gui.inicio import mostrar_pantalla_inicio
from database.db import inicializar_y_agregar_adivinanzas

# Función principal del programa
def main():
    inicializar_y_agregar_adivinanzas()
    inicializar_db()
    mostrar_pantalla_inicio()

if __name__ == "__main__":
    main()
