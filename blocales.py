#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
blocales.py
------------

Algoritmos generales para búsquedas locales

"""

__author__ = 'juliowaissman'


from math import exp
from random import random


class Problema(object):
    """
    Definición formal de un problema de búsqueda local. Es necesario adaptarla a
    cada problema en específico, en particular:

    a) Todos los métodos requieren de implementar costo y estado_aleatorio

    b) descenso_colinas  requiere de implementar el método vecinos

    c) temple_simulado requiere vecino_aleatorio

    """
    def estado_aleatorio(self):
        """
        @return Una tupla que describe un estado

        """
        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")

    def vecinos(self, estado):
        """
        Generador de los vecinos de un estado

        @param estado: Una tupla que describe un estado

        @return: Un generador de estados vecinos (utilizar yield en lugar de return)

        """
        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado en forma aleatoria. Procurar generar el estado  vecino
        a partir de una distribución uniforme de ser posible.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.
        """
        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")

    def costo(self, estado):
        """
        Calcula el costo de un estado dado

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")


def descenso_colinas(problema, maxit=1000000):
    """
    Busqueda local por descenso de colinas.

    @param problema: Un objeto de una clase heredada de blocales.Problema
    @param maxit: Máximo número de iteraciones

    @return: El estado con el menor costo encontrado

    """
    estado = problema.estado_aleatorio()
    costo = problema.costo(estado)

    for _ in xrange(maxit):
        e = min(problema.vecinos(estado), key=problema.costo)
        c = problema.costo(e)
        if c >= costo:
            break
        estado, costo = e, c
    return estado


def temple_simulado(problema, calendarizador=lambda i: cal_expon(i, 100, 0.01), maxit=1000000):
    """
    Busqueda local por temple simulado

    @param problema: Un objeto de una clase heredada de blocales.Problema
    @param calendarizador: Una función que recibe la iteración y devuelve la temperatura
    @param maxit: Máximo número de iteraciones

    @return: El estado con el menor costo encontrado

    """

    estado = problema.estado_aleatorio()
    costo = problema.costo(estado)
    
    e_mejor, c_mejor = estado, costo

    for i in xrange(maxit):
        temperatura = calendarizador(i)
        if temperatura < 1e-8:
            break

        vecino = problema.vecino_aleatorio(estado)
        costo_vecino = problema.costo(vecino)
        error = costo - costo_vecino

        if error > 0 or random() < exp(error / temperatura):
            estado, costo = vecino, costo_vecino
        
            if c_mejor - costo > 0:
                e_mejor, c_mejor = estado, costo

    return e_mejor
    #return estado


def cal_expon(iteracion, K=100, delta=0.01):
    """
    Calendarizador exponencial

    Aplica la formula temperatura = K * exp(-delta * iteracion)

    @param iteracion: Un entero con la iteración (empezando por 0)
    @param K: Valor de temperatura en la primer iteración
    @param delta: Variación exponencial (4 veces delta es .1 el valor de K)

    @return: Un flotante con la temperatura a esa iteración

    """
    return K * exp(-delta * iteracion)