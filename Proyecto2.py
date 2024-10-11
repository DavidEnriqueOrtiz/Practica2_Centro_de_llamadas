#Rivera Paz Valeria
#Ortiz Gonzalez David Enrique
#Vasquez Hernandez Griselda
import random

class Cliente:
    def __init__(self, tiempo_llegada, tiempo_atencion, es_premier):
        #inicializar el cliente con tiempo de llegada, atencion y si es premier
        self.llegada = tiempo_llegada
        self.atencion = tiempo_atencion
        self.premier = es_premier

class Simulacion:
    def __init__(self, lineas):
        #inicializar la simulacion con numero de lineas y colas vacias
        self.lineas = lineas
        self.cola_premier = []  #lista para clientes premier
        self.cola_regular = []  #lista para clientes regulares
        self.disponibles = lineas
        self.tiempo = 0
        self.max_espera_premier = 0

    def generar_cliente(self):
        #generar un cliente con tiempos aleatorios y si es premier
        atencion = random.randint(1, 81)  #tiempo de atencion aleatorio
        es_premier = random.randint(1, 6) == 1  #uno de cada seis es premier
        return Cliente(self.tiempo, atencion, es_premier)

    def agregar_cliente(self, cliente):
        #agregar cliente a la cola correspondiente
        if cliente.premier:
            self.cola_premier.append(cliente)
        else:
            self.cola_regular.append(cliente)

    def atender_clientes(self):
        #atender a todos los clientes posibles con las lineas disponibles
        while self.disponibles > 0 and (self.cola_premier or self.cola_regular):
            #atender clientes premier primero si hay
            if self.cola_premier:
                cliente = self.cola_premier.pop(0)  #atender primer cliente premier
            else:
                cliente = self.cola_regular.pop(0)  #atender primer cliente regular

            espera = self.tiempo - cliente.llegada  #calcular tiempo de espera
            if cliente.premier:
                self.max_espera_premier = max(self.max_espera_premier, espera)  #actualizar max espera premier

            self.disponibles -= 1  #ocupar una linea

    def liberar_lineas(self, ocupadas):
        #actualizar las lineas y liberar las que terminan atencion
        ocupadas = [t - 1 for t in ocupadas if t > 0]  #disminuir tiempos de atencion
        self.disponibles = self.lineas - len(ocupadas)  #recalcular lineas disponibles
        return ocupadas

    def correr(self, duracion):
        ocupadas = []  #lista para manejar lineas ocupadas
        proxima_llegada = random.randint(1, 3)  #proximo cliente llega en 1 a 3 minutos

        for _ in range(duracion):
            self.tiempo += 1  #avanza el tiempo

            #si es tiempo de llegada de un cliente, se agrega a la cola
            if self.tiempo == proxima_llegada:
                cliente = self.generar_cliente()
                self.agregar_cliente(cliente)
                proxima_llegada = self.tiempo + random.randint(1, 3)  #calcular nueva llegada

            #atender clientes y actualizar lineas ocupadas
            self.atender_clientes()
            while len(ocupadas) < self.lineas - self.disponibles:
                ocupadas.append(random.randint(1, 81))  #nueva linea ocupada con tiempo aleatorio

            #liberar lineas ocupadas que terminen su tiempo
            ocupadas = self.liberar_lineas(ocupadas)

        return self.max_espera_premier  #devolver tiempo maximo de espera premier

if __name__ == "__main__":
    duracion_simulacion = 24 * 60  #24 horas en minutos
    objetivo_espera = 15  #tiempo maximo deseado para clientes premier

    #probar diferentes cantidades de lineas para encontrar el minimo
    for lineas in range(19, 50):
        sim = Simulacion(lineas)
        max_espera = sim.correr(duracion_simulacion)

        print(f"Lineas: {lineas}, Maxima espera: {max_espera} minutos")

        if max_espera <= objetivo_espera:
            print(f"\nMinimo de lineas necesarias: {lineas}")
            print(f"Tiempo maximo estimado para premier: {max_espera} minutos")
            break
    else:
        print("\nNo se logro cumplir con el tiempo objetivo en las lineas probadas.")
