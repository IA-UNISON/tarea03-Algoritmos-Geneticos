#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'juliowaissman'


import blocales
from random import shuffle
from random import sample
from itertools import permutations
from itertools import combinations
from math import exp


class ProblemaNreinas(blocales.Problema):
    """
    Las N reinas en forma de búsqueda local se inicializa como

    entorno = ProblemaNreinas(n) donde n es el número de reinas a colocar

    Por default son las clásicas 8 reinas.

    """
    def __init__(self, n=8):
        self.n = n

    def estado_aleatorio(self):
        estado = range(self.n)
        shuffle(estado)
        return tuple(estado)

    def vecinos(self, estado):
        """
        Generador de los vecinos de un estado, permutando de dos en dos posiciones

        @param estado: Una tupla que describe un estado

        @return: Un generador de estados vecinos (utilizar yield en lugar de return)

        """
        edo_lista = list(estado)
        for i, j in permutations(xrange(self.n), 2):
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]
            yield tuple(edo_lista)
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado intercambiando dos posiciones en forma aleatoria.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.
        """
        vecino = list(estado)
        i, j = sample(range(self.n), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return tuple(vecino)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        c = 0
        for i, j in combinations(range(self.n), 2):
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(j-i):
                c += 1
        return c


def prueba_descenso_colinas(problema=ProblemaNreinas(8), repeticiones=10):
    """ Prueba el algoritmo de descenso de colinas con n repeticiones """

    print "\n\n" + "intento".center(10) + "estado".center(60) + "costo".center(10)
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
        print str(intento).center(10) + str(solucion).center(60) + str(problema.costo(solucion)).center(10)


def prueba_temple_simulado(problema=ProblemaNreinas(8), K=100, delta=0.01):
    """ Prueba el algoritmo de temple simulado con calendarizador exponencial """

    solucion = blocales.temple_simulado(problema, lambda i: K * exp(-delta * i))
    print u"\n\nUtilizando temple simulado con calendarización exponencial"
    print "K= ", K, " y delta= ", delta
    print u"\nEl costo de la solución utilizando temple simulado es ", problema.costo(solucion)
    print u"Y la solución es: "
    print solucion


if __name__ == "__main__":

    #prueba_descenso_colinas(ProblemaNreinas(32), 10)
    prueba_temple_simulado(ProblemaNreinas(64), 500, 0.01)