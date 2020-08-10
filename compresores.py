import numpy as np
import matplotlib.pyplot as plt


class Compresor:

    def __init__(self, potencia, etapas):
        self.potencia = potencia    # Potencia del compresor
        self.estado = False      # Compresor encendido o parado
        self._disponible_on = True      # Puedo arrancar
        self._disponible_off = False    # Puedo parar
        self.tiempo = 0          # Tiempo de la simulacion [s]
        self.tiempo_aux = 0      # Variable auxiliar de tiempo [s]
        self.tiempo_off = 0      # Tiempo que lleva parado el compresor [s]
        self.tiempo_on = 0       # Tiempo que lleva encendido el compresor [s]
        self.etapas = etapas     # Número de etapas []
        self.etapas_activas = 0  # Número de etapas activas []
        self.potencia_etapa = potencia/etapas

        # Tiempos entre starts y stops
        self.t_start_start = 0
        self.t_start_stop = 0
        self.t_start_etapas = 0

    def aumentar_tiempo(self, paso):
        self.tiempo += paso
        self.tiempo_aux += paso
        if self.estado is True:
            self.tiempo_on += paso
        else:
            self.tiempo_off += paso

    def disponible_on(self):
        '''
        Si está disponible para encender, es por que está apagado
        '''
        ciclo = self.tiempo_on + self.tiempo_off
        _disponible_on = self._disponible_on
        t = self.tiempo
        t_start_start = self.t_start_start
        t_start_stop = self.t_start_stop
        estado = self.estado

        if (_disponible_on is False) and (ciclo >= t_start_start):
            _disponible_on = True
        elif tiempo < max(t_start_start, t_start_stop) and not estado:
            _disponible_on = True
        else:
            _disponible_on = False
        self._disponible_on = _disponible_on

        return self._disponible_on

    def disponible_off(self):
        if self.estado is True:
            if self.tiempo_on >= self.t_start_stop:
                self._disponible_off = True
            else:
                self._disponible_off = False
        return self._disponible_off

    def establecer_estado(self, estado):
        self.tiempo_aux = 0
        self.estado = estado    # True o False si está encendido o no
        # Si lo enciendo es por que estaba apagado
        if estado is True:
            self.etapas_activas = 1
            self.tiempo_on = 0
            self.tiempo_off = self.tiempo
            self.disponible_on()
        else:
            self.etapas_activas = 0
            self.tiempo_on = self.tiempo
            self.tiempo_off = 0
            self.disponible_off()


def set_tiempos(compresores, start_start, start_stop, start_etapas):

    for i in range(len(compresores)):
        compresores[i].t_start_start = start_start
        compresores[i].t_start_stop = start_stop
        compresores[i].t_start_etapas = start_etapas


paso = 1
numero_compresores = 4
numero_etapas = 4

# Parámetros de gestión de los compresores
t_start_start = 300              # [s]
t_start_stop = 240               # [s]
t_start_compresores = 30         # [s]
t_start_etapas = 5               # [s]

compresor = [None]*numero_compresores

for i in range(4):
    compresor[i] = Compresor(potencia=125, etapas=numero_etapas)

compresor[0].estado = True
set_tiempos(compresor, t_start_start, t_start_stop, t_start_etapas)

tiempo = 0
t = np.linspace(0, 499, 500)
disponibilidad = np.zeros((500, 4))
while tiempo < 500:
    for i in range(4):
        compresor[i].aumentar_tiempo(paso)
        disponibilidad[tiempo, i] = compresor[i].disponible_on()
    tiempo += 1

plt.plot(t, disponibilidad[:, 0])
plt.plot(t, disponibilidad[:, 1])
plt.plot(t, disponibilidad[:, 2])
plt.plot(t, disponibilidad[:, 3])
plt.legend(["Compresor 1", "Compresor 2", "Compresor 3", "Compresor 4"])
plt.show()
