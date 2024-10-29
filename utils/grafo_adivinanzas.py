import networkx as nx
import random

# Clase que representa un grafo de adivinanzas
class GrafoAdivinanzas:
    # Constructor de la clase
    def __init__(self, max_adivinanzas=3):
        # Inicializa un grafo dirigido vacío
        self.grafo = nx.DiGraph()
        # Conjunto para almacenar las adivinanzas ya respondidas
        self.adivinanzas_respondidas = set()
        # Número máximo de adivinanzas a presentar
        self.max_adivinanzas = max_adivinanzas

    # Método para agregar una adivinanza al grafo
    def agregar_adivinanza(self, id_adivinanza, adivinanza):
        # Agrega un nodo al grafo con el ID de la adivinanza y su contenido
        self.grafo.add_node(id_adivinanza, adivinanza=adivinanza)

    # Método para conectar dos adivinanzas
    def conectar_adivinanzas(self, id_origen, id_destino):
        # Agrega una arista dirigida entre dos adivinanzas
        self.grafo.add_edge(id_origen, id_destino)

    # Método para marcar una adivinanza como respondida
    def marcar_como_respondida(self, id_adivinanza):
        # Marca una adivinanza como respondida
        self.adivinanzas_respondidas.add(id_adivinanza)

    # Método para obtener la siguiente adivinanza
    def obtener_siguiente_adivinanza(self):
        # Obtiene una adivinanza aleatoria que no haya sido respondida aún
        adivinanzas_disponibles = [n for n in self.grafo.nodes() if n not in self.adivinanzas_respondidas]
        if not adivinanzas_disponibles:
            return None
        return random.choice(adivinanzas_disponibles)

    # Método para verificar si todas las adivinanzas han sido respondidas
    def todas_respondidas(self):
        # Verifica si todas las adivinanzas han sido respondidas
        return len(self.adivinanzas_respondidas) == len(self.grafo.nodes())

    # Método para obtener el contenido de una adivinanza
    def obtener_adivinanza(self, id_adivinanza):
        # Obtiene el contenido de una adivinanza específica
        return self.grafo.nodes[id_adivinanza]['adivinanza']

    # Método para reiniciar el grafo de adivinanzas#
    def reiniciar(self):
        # Reinicia el conjunto de adivinanzas respondidas
        self.adivinanzas_respondidas.clear()

    # Métodos para obtener el total de adivinanzas
    def total_adivinanzas(self):
        # Retorna el número total de adivinanzas a presentar
        # (limitado por max_adivinanzas o por las adivinanzas disponibles)
        return min(self.max_adivinanzas, len(self.grafo.nodes()) - len(self.adivinanzas_respondidas))

    # Método para obtener el número de adivinanzas restantes
    def adivinanzas_restantes(self):
        # Retorna el número de adivinanzas que aún no han sido respondidas
        return len(self.grafo.nodes()) - len(self.adivinanzas_respondidas)
