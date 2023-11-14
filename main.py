import networkx as nx
import matplotlib.pyplot as plt

class Nodo:
    def _init_(self, nombre, ubicacion, tipo, demanda=None):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.tipo = tipo
        self.demanda = demanda

class Ruta:
    def _init_(self, origen, destino, distancia, capacidad):
        self.origen = origen
        self.destino = destino
        self.distancia = distancia
        self.capacidad = capacidad

class DistribucionAlimentos:
    def _init_(self):
        self.nodos = {}
        self.rutas = {}
        self.grafo_networkx = nx.Graph()

    def agregar_nodo(self, nombre, ubicacion, tipo, demanda=None):
        nodo = Nodo(nombre, ubicacion, tipo, demanda)
        self.nodos[nombre] = nodo
        self.grafo_networkx.add_node(nombre, ubicacion=ubicacion, tipo=tipo, demanda=demanda)

    def agregar_ruta(self, origen, destino, distancia, capacidad):
        ruta = Ruta(origen, destino, distancia, capacidad)
        self.rutas[(origen, destino)] = ruta
        self.grafo_networkx.add_edge(origen, destino, distancia=distancia, capacidad=capacidad)

    def visualizar_grafo(self):
        posiciones = nx.get_node_attributes(self.grafo_networkx, 'ubicacion')
        nx.draw(self.grafo_networkx, posiciones, with_labels=True)
        plt.show()

    def dijkstra(self, origen, destino):
        distancias = {nodo: float('inf') for nodo in self.nodos}
        distancias[origen] = 0
        visitados = set()

        while visitados != set(distancias):
            nodo_actual = min(set(distancias) - visitados, key=distancias.get)
            visitados.add(nodo_actual)

            for ruta in self.rutas.values():
                if ruta.origen == nodo_actual and ruta.destino not in visitados:
                    nueva_distancia = distancias[nodo_actual] + ruta.distancia
                    if nueva_distancia < distancias[ruta.destino]:
                        distancias[ruta.destino] = nueva_distancia

        mejor_ruta = [destino]
        while mejor_ruta[-1] != origen:
            for ruta in self.rutas.values():
                if ruta.destino == mejor_ruta[-1] and distancias[ruta.destino] == distancias[ruta.origen] + ruta.distancia:
                    mejor_ruta.append(ruta.origen)
                    break

        return mejor_ruta[::-1]

# Función para interactuar con el usuario
def interactuar_con_usuario():
    distribucion = DistribucionAlimentos()

    while True:
        print("\n1. Agregar Nodo")
        print("2. Agregar Ruta")
        print("3. Visualizar Grafo")
        print("4. Calcular Mejor Ruta")
        print("5. Salir")

        opcion = int(input("\nIngrese la opción: "))

        if opcion == 1:
            nombre = input("Ingrese el nombre del nodo: ")
            ubicacion = tuple(map(float, input("Ingrese la ubicación (latitud, longitud): ").split(',')))
            tipo = input("Ingrese el tipo del nodo (almacen/punto_venta): ")
            demanda = int(input("Ingrese la demanda (solo para puntos de venta): ")) if tipo == 'punto_venta' else None

            distribucion.agregar_nodo(nombre, ubicacion, tipo, demanda)
            print(f"Se ha agregado el nodo {nombre}.")

        elif opcion == 2:
            origen = input("Ingrese el nombre del nodo de origen: ")
            destino = input("Ingrese el nombre del nodo de destino: ")
            distancia = float(input("Ingrese la distancia entre los nodos: "))
            capacidad = float(input("Ingrese la capacidad de la ruta: "))

            distribucion.agregar_ruta(origen, destino, distancia, capacidad)
            print(f"Se ha agregado la ruta entre {origen} y {destino}.")

        elif opcion == 3:
            distribucion.visualizar_grafo()

        elif opcion == 4:
            origen = input("Ingrese el nombre del nodo de origen: ")
            destino = input("Ingrese el nombre del nodo de destino: ")

            try:
                mejor_ruta = distribucion.dijkstra(origen, destino)
                print(f"La mejor ruta entre {origen} y {destino} es: {mejor_ruta}")
            except KeyError:
                print(f"No hay ruta entre {origen} y {destino}.")

        elif opcion == 5:
            break

        else:
            print("Opción no válida. Inténtelo de nuevo.")

if _name_ == "_main_":
    interactuar_con_usuario()
