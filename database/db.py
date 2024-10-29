import mysql.connector
from database.mysql_connection import conectar_mysql

# Función para inicializar la base de datos creando la tabla Adivinanzas si no existe
def inicializar_adivinanzas():
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Adivinanzas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        texto TEXT NOT NULL,
        respuesta TEXT NOT NULL,
        categoria TEXT NOT NULL,
        estado BOOLEAN DEFAULT FALSE
    )
    ''')
    conn.commit()
    conn.close()

# Función para insertar adivinanzas en la base de datos si no existen
def insertar_adivinanzas(adivinanzas):
    conn = conectar_mysql()
    cursor = conn.cursor()
    for pregunta, respuesta, categoria in adivinanzas:
        # Verificar si la adivinanza ya existe
        cursor.execute('''
        SELECT COUNT(*) FROM Adivinanzas WHERE texto = %s AND respuesta = %s AND categoria = %s
        ''', (pregunta, respuesta, categoria))
        if cursor.fetchone()[0] == 0:
            # Insertar solo si la adivinanza no existe
            cursor.execute('''
            INSERT INTO Adivinanzas (texto, respuesta, categoria)
            VALUES (%s, %s, %s)
            ''', (pregunta, respuesta, categoria))
    conn.commit()
    conn.close()

# Lista de adivinanzas
adivinanzas = [
    # Animales
    ("Soy verde y salto, salto sin parar. En las charcas vivo y sé croar. ¿Quién soy?", "la rana", "Animales"),
    ("Tengo cuello largo, manchas en la piel, y en África vivo. ¿Sabes quién soy?", "la jirafa", "Animales"),
    ("Vuelo de noche, duermo de día y no soy un ave. ¿Quién podría ser?", "el murciélago", "Animales"),
    ("Soy naranja con rayas negras, feroz y elegante. En la selva soy el rey. ¿Quién soy?", "el tigre", "Animales"),
    ("Tengo trompa y colmillos, soy grande y gris. En la sabana vivo feliz. ¿Quién soy?", "el elefante", "Animales"),
    ("Soy peludo y pequeño, con bigotes y cola larga. Cazo ratones y me gusta maullar. ¿Quién soy?", "el gato", "Animales"),
    ("En el mar nado veloz, tengo aleta dorsal. A veces salto fuera del agua. ¿Quién soy?", "el delfín", "Animales"),
    ("Soy el rey de la selva, con melena dorada. Mi rugido es potente. ¿Quién soy?", "el león", "Animales"),
    ("Tengo plumas de colores y puedo hablar. En una jaula suelo estar. ¿Quién soy?", "el loro", "Animales"),
    ("Soy blanco y suave, en la granja vivo. Doy lana para tu ropa. ¿Quién soy?", "la oveja", "Animales"),

    # Comida
    ("Soy roja por fuera, blanca por dentro. Si me muerdes, refrescante me encuentro. ¿Qué soy?", "la sandía", "Comida"),
    ("Me hacen con leche, me comen los ratones. En trozos o lonchas doy sabor a tus opciones. ¿Qué soy?", "el queso", "Comida"),
    ("Soy amarillo por fuera, blanco por dentro. Para comerme, me tienes que pelar. ¿Qué soy?", "el plátano", "Comida"),
    ("Tengo escamas pero no soy pez, tengo corona pero no soy rey. ¿Qué soy?", "la piña", "Comida"),
    ("Soy redonda y aplastada, en el horno me calientan. Con queso y tomate me alimentan. ¿Qué soy?", "la pizza", "Comida"),
    ("Soy verde y larguirucha, y mi nombre empieza por P. Si no me comes, te pondrás como un palillo. ¿Qué soy?", "el pepino", "Comida"),
    ("Oro parece, plata no es. Abre las cortinas y verás lo que es. ¿Qué soy?", "el plátano", "Comida"),
    ("Blanca soy, del agua nací, pobres y ricos comen de mí. ¿Qué soy?", "la sal", "Comida"),
    ("Me pisas y no me quejo, me comen y desaparezco. ¿Qué soy?", "la uva", "Comida"),
    ("Soy roja y dulce, con semillas por fuera. En tartas y postres soy la primera. ¿Qué soy?", "la fresa", "Comida"),

    # Naturaleza
    ("Vuela sin alas, llora sin ojos. ¿Qué es?", "la nube", "Naturaleza"),
    ("Sube y baja sin moverse de su sitio. ¿Qué es?", "la marea", "Naturaleza"),
    ("Corro y me escondo, y no me ves. Silbo y me sientes, pero no me puedes coger. ¿Qué soy?", "el viento", "Naturaleza"),
    ("De día soy blanca, de noche soy negra. Cuando llueve soy gris. ¿Qué soy?", "la montaña", "Naturaleza"),
    ("No tengo pies, pero corro. No tengo boca, pero rujo. ¿Qué soy?", "el río", "Naturaleza"),
    ("Verde por fuera, verde por dentro, con una capita en el centro. ¿Qué es?", "la pera", "Naturaleza"),
    ("Mil soldados en fila, ninguno se ve la espalda. ¿Qué son?", "los árboles del bosque", "Naturaleza"),
    ("Tengo hojas sin ser árbol, lomo sin ser caballo. ¿Qué soy?", "el libro", "Naturaleza"),
    ("Vuelo sin alas, lloro sin ojos. Oscurezco el cielo, hago caer agua. ¿Qué soy?", "la nube de lluvia", "Naturaleza"),
    ("Soy alta cuando soy joven y baja cuando soy vieja. ¿Qué soy?", "la vela", "Naturaleza"),

    # Ciencia
    ("Soy un planeta enano, fui degradado. Antes era el noveno, ahora estoy apartado. ¿Quién soy?", "plutón", "Ciencia"),
    ("Soy el rey del sistema solar, brillo con fuerza y doy calor. ¿Quién soy?", "el sol", "Ciencia"),
    ("Soy invisible, pero vital. Sin mí, no podrías respirar. ¿Qué soy?", "el oxígeno", "Ciencia"),
    ("Tengo agujas, pero no coso. Tengo números, pero no soy matemático. ¿Qué soy?", "el reloj", "Ciencia"),
    ("Soy el planeta rojo, cuarto desde el Sol. Marte es mi nombre, ¿lo sabes o no?", "marte", "Ciencia"),
    ("Sin mí, los aviones no podrían volar. Soy invisible, pero me puedes sentir. ¿Qué soy?", "el aire", "Ciencia"),
    ("Soy el líquido más abundante en la Tierra. Sin mí, la vida no existiría. ¿Qué soy?", "el agua", "Ciencia"),
    ("Soy una fuerza que te mantiene en el suelo. Sin mí, florarías en el espacio. ¿Qué soy?", "la gravedad", "Ciencia"),
    ("Soy un gas noble, brillo en los letreros. En los globos me usan para hacerlos ligeros. ¿Qué soy?", "el helio", "Ciencia"),
    ("Soy el proceso por el que las plantas hacen su comida usando luz solar. ¿Qué soy?", "la fotosíntesis", "Ciencia"),

    # Deportes
    ("Tengo red, pero no pesco. Tengo cuadros, pero no soy tablero. ¿Qué deporte soy?", "el tenis", "Deportes"),
    ("Me lanzan, me golpean y me patean. Redondo soy y en la portería entro. ¿Qué soy?", "el balón de fútbol", "Deportes"),
    ("Sobre hielo me deslizo, con cuchillas en los pies. Giro y salto sin caer. ¿Qué deporte soy?", "el patinaje artístico", "Deportes"),
    ("Con un palo largo y una pelota pequeña, en el green me encuentras. ¿Qué deporte soy?", "el golf", "Deportes"),
    ("En el agua me muevo, brazadas doy sin parar. De un extremo a otro voy. ¿Qué deporte soy?", "la natación", "Deportes"),
    ("Salto alto, salto largo, corro rápido en la pista. ¿Qué conjunto de deportes soy?", "el atletismo", "Deportes"),
    ("Dos equipos, una canasta alta. Botando y lanzando, puntos se marcan. ¿Qué deporte soy?", "el baloncesto", "Deportes"),
    ("Sobre ruedas me muevo, trucos hago sin parar. En el parque o en la calle, me puedes encontrar. ¿Qué soy?", "el skateboard", "Deportes"),
    ("Con raquetas se juega, pero no es tenis. Sobre una mesa se desarrolla el juego. ¿Qué deporte soy?", "el ping-pong", "Deportes"),
    ("En el ring me encuentro, con guantes golpeo. Esquivo y ataco en cada asalto. ¿Qué deporte soy?", "el boxeo", "Deportes"),

    # Geografía
    ("Soy el continente más grande, hogar de la Gran Muralla. ¿Cuál soy?", "asia", "Geografía"),
    ("Soy una isla y un continente a la vez. Canguros y koalas viven en mi tierra. ¿Quién soy?", "australia", "Geografía"),
    ("Soy el río más largo del mundo, fluyo por el norte de África. ¿Cuál soy?", "el nilo", "Geografía"),
    ("Soy la cordillera más larga del mundo, recorro Sudamérica de norte a sur. ¿Quién soy?", "los andes", "Geografía"),
    ("Soy el océano más grande, ocupo casi un tercio de la superficie terrestre. ¿Cuál soy?", "el océano pacífico", "Geografía"),
    ("Soy el desierto más grande del mundo, cubro gran parte del norte de África. ¿Cuál soy?", "el sahara", "Geografía"),
    ("Soy la selva tropical más grande del planeta, hogar de innumerables especies. ¿Quién soy?", "el amazonas", "Geografía"),
    ("Soy el punto más alto de la Tierra, mi cima está en el Himalaya. ¿Quién soy?", "el monte everest", "Geografía"),
    ("Soy un país con forma de bota, famoso por mi pasta y pizza. ¿Quién soy?", "italia", "Geografía"),
    ("Soy un archipiélago en forma de arco en el Pacífico, famoso por mis samuráis y sushi. ¿Quién soy?", "japón", "Geografía"),

    # Cuentos y Fábulas
    ("Soy una niña de capa roja que visita a su abuela en el bosque. ¿Quién soy?", "caperucita roja", "Cuentos y Fábulas"),
    ("Soy un muñeco de madera cuya nariz crece cuando miento. ¿Quién soy?", "pinocho", "Cuentos y Fábulas"),
    ("Somos dos hermanos perdidos en el bosque que encuentran una casa de dulces. ¿Quiénes somos?", "hansel y gretel", "Cuentos y Fábulas"),
    ("Soy una princesa que duerme por cien años hasta que un príncipe me despierta. ¿Quién soy?", "la bella durmiente", "Cuentos y Fábulas"),
    ("Soy un ogro verde que vive en un pantano y me enamoro de una princesa. ¿Quién soy?", "shrek", "Cuentos y Fábulas"),
    ("Soy una sirena que quiere ser humana para estar con su príncipe. ¿Quién soy?", "la sirenita", "Cuentos y Fábulas"),
    ("Soy un gato con botas que ayuda a su amo a convertirse en un marqués. ¿Quién soy?", "el gato con botas", "Cuentos y Fábulas"),
    ("Soy una joven que pierde su zapato de cristal en un baile real. ¿Quién soy?", "cenicienta", "Cuentos y Fábulas"),
    ("Soy un oso que ama la miel y vive en el Bosque de los Cien Acres. ¿Quién soy?", "winnie the pooh", "Cuentos y Fábulas"),
    ("Somos tres cerditos que construimos casas para protegernos del lobo. ¿Quiénes somos?", "los tres cerditos", "Cuentos y Fábulas"),

    # Historia
    ("Fui el primer presidente de los Estados Unidos. ¿Quién soy?", "george washington", "Historia"),
    ("Descubrí América en 1492. ¿Quién soy?", "cristóbal colón", "Historia"),
    ("Fui la reina de Egipto, famosa por mi belleza y astucia. ¿Quién soy?", "cleopatra", "Historia"),
    ("Pinté la Mona Lisa y diseñé muchos inventos. ¿Quién soy?", "leonardo da vinci", "Historia"),
    ("Lideré la revolución cubana y goberné Cuba por décadas. ¿Quién soy?", "fidel castro", "Historia"),
    ("Fui el líder de la India en la lucha por la independencia, famoso por la no violencia. ¿Quién soy?", "mahatma gandhi", "Historia"),
    ("Fui la primera mujer en volar sola a través del Atlántico. ¿Quién soy?", "amelia earhart", "Historia"),
    ("Lideré el movimiento por los derechos civiles en Estados Unidos. Tengo un sueño. ¿Quién soy?", "martin luther king jr.", "Historia"),
    ("Fui el primer hombre en pisar la Luna. ¿Quién soy?", "neil armstrong", "Historia"),
    ("Fui la 'Dama de Hierro', primera ministra del Reino Unido. ¿Quién soy?", "margaret thatcher", "Historia")
]

# Inicializar la tabla de adivinanzas y agregar las adivinanzas
def inicializar_y_agregar_adivinanzas():
    inicializar_adivinanzas()
    insertar_adivinanzas(adivinanzas)
