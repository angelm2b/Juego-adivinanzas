import mysql.connector
import json

# Función para establecer la conexión con la base de datos MySQL
def conectar_mysql():
    return mysql.connector.connect(
        user='nombre_usuario', 
        password='contraseña', 
        host='127.0.0.1', 
        database='nombre_base_de_datos'
    )

# Función para inicializar la base de datos creando la tabla Progreso si no existe
def inicializar_db():
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Progreso (
        nombre VARCHAR(255),
        categoria VARCHAR(255),
        puntos INT,
        intentos INT,
        adivinanzas_respondidas TEXT,
        PRIMARY KEY (nombre, categoria)
    )
    ''')
    conn.commit()
    conn.close()


# Función para obtener el progreso de un jugador
def obtener_progreso(nombre_jugador, categoria=None):
    conn = conectar_mysql()
    cursor = conn.cursor(dictionary=True)
    if categoria:
        # Si se especifica una categoría, busca el progreso específico
        cursor.execute("SELECT * FROM Progreso WHERE nombre = %s AND categoria = %s", (nombre_jugador, categoria))
    else:
        # Si no se especifica categoría, obtiene todo el progreso del jugador
        cursor.execute("SELECT * FROM Progreso WHERE nombre = %s", (nombre_jugador,))
    resultados = cursor.fetchall()
    conn.close()
    # Convierte las adivinanzas respondidas de JSON a lista de Python
    for resultado in resultados:
        if resultado:
            resultado['adivinanzas_respondidas'] = json.loads(resultado['adivinanzas_respondidas'])
    # Devuelve los resultados según si se especificó una categoría o no
    return resultados if categoria is None else resultados[0] if resultados else None

# Función para guardar o actualizar el progreso de un jugador
def guardar_progreso(nombre_jugador, categoria, progreso):
    conn = conectar_mysql()
    cursor = conn.cursor()
    
    # Inserta o actualiza el progreso en la tabla
    cursor.execute("""
        INSERT INTO Progreso (nombre, categoria, puntos, intentos, adivinanzas_respondidas)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        puntos = VALUES(puntos),
        intentos = VALUES(intentos),
        adivinanzas_respondidas = VALUES(adivinanzas_respondidas)
    """, (nombre_jugador, categoria, progreso["puntos"], progreso["intentos"], json.dumps(progreso["adivinanzas_respondidas"])))
    
    conn.commit()
    conn.close()

