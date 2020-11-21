"""
Algoritmo MedianCut
Las ideas y mejor explicacion tomados de http://joelcarlson.github.io/2016/01/15/median-cut/
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as plt


class Cubo():
    """
    Clase que implementa el cubo de medianCut
    """
    def __init__(self, datos, items):
        """
        Crea la clase con los datos de la imagen y el conjunto de pixeles que 
        componen el cubo.
        Los pixeles que conforman el cubo son una lista con el indice del pixeles
        """
        self.datos = datos
        self.items = items
        self.rangoR = self.calcularRango(0) 
        self.rangoG = self.calcularRango(1)
        self.rangoB = self.calcularRango(2)
        
        self.medianaR = self.calcularMediana(0) 
        self.medianaG = self.calcularMediana(1)
        self.medianaB = self.calcularMediana(2)
        
        self.mayorRango = np.max([self.rangoR, self.rangoG, self.rangoB])
        self.mayorCanal = np.argmax([self.rangoR, self.rangoG, self.rangoB])
        
    def calcularRango(self, canal):
        """
        Calcula el rango (max - min) de un canal de los datos que conforman
        el cubo
        """
        return np.max(self.datos[self.items, canal]) - np.min(self.datos[self.items, canal])
        
    def calcularMediana(self, canal):
        """
        Calcula la mediana de los valores de un canal de los datos que conforman
        el cubo
        """
        return np.median(self.datos[self.items, canal])
    
    def dividir(self):
        """
        Devuelve dos objetos cubo repartiendo los datos que conforman el cubo.
        La repartición se realiza diviendo los pixeles entre los valores mas altos
        que la mediana del canal con mas rango y los valores mas bajos
        """
        valor = self.calcularMediana(self.mayorCanal)
        _ = np.where(self.datos[self.items, self.mayorCanal] <= valor)
        itemsDebajo = self.items[_]
        _ = np.where(self.datos[self.items, self.mayorCanal] > valor)
        itemsArriba = self.items[_] 
        return Cubo(self.datos, itemsDebajo), Cubo(self.datos, itemsArriba)
        
    def __str__(self):
        """
        Representa:
        id del objeto, Max(Canal Rojo) - Min(Canal Rojo),
                       Max(Canal Verde) - Min(Canal Verde),
                       Max(Canal Azul) - Min(Canal Azul),
                       Componentes totales del cubo
        """ 
        cadena = "{}\t{}-{}\t{}-{}\t{}-{}\t{}".format(
            id(self),
            np.max(self.datos[self.items, 0]), np.min(self.datos[self.items, 0]),
            np.max(self.datos[self.items, 1]), np.min(self.datos[self.items, 1]),
            np.max(self.datos[self.items, 2]), np.min(self.datos[self.items, 2]),
            self.items.shape[0])
        return cadena

# Leer imagen
datos = plt.imread('.\images\Graffiti.jpg')
# convertir a ndim=2
datos = datos.reshape(datos.shape[0] * datos.shape[1], datos.shape[2])
# definir colores 
n_colores = 64
verbose = True
#Crear lista de cubos
cubos = []

primercubo = Cubo(datos, np.arange(datos.shape[0]))
cubos.append(primercubo)

for iteracion in range(n_colores - 1):
    rangos = np.array([item.mayorRango for item in cubos])
    cuboseleccionado = cubos[np.argmax(rangos)]
    cubos.pop(np.argmax(rangos))  # no me interesa porque al dividir creo dos 
                                  # a partir de este, por eso se elimina
    cubo1, cubo2 = cuboseleccionado.dividir()
    cubos.append(cubo1)
    cubos.append(cubo2)
    print("Iteracion {}".format(iteracion))
    print("\t\tRangoR\tRangoG\tRangoB\tItems")
    if verbose: _ = [print(item) for item in cubos]

# Recuperar los colores, usando la mediana de cada canal de cada cubo
resultado = np.zeros_like(datos)
for cubo in cubos:
    resultado[cubo.items] = np.array([cubo.medianaR, cubo.medianaG, cubo.medianaB])

resultado = resultado.reshape(datos.shape)
fig, ax = plt.subplots(1, 1, figsize=(17, 7))
ax.imshow(resultado)
plt.show()
