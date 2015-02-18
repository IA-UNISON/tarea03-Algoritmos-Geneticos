#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
genetico.py
------------

Este modulo incluye el algoritmo genérico para algoritmos genéticos, así como un
algoritmo genético adaptado a problemas de permutaciones, como el problema de las
n-reinas o el agente viajero.

Como tarea se pide desarrollar otro algoritmo genético con el fin de probar otro tipo
de métodos internos, así como ajustar ambos algortmos para que funcionen de la mejor
manera posible.


Para que funcione, este modulo debe de encontrarse en la misma carpeta que blocales.py
y nreinas.py vistas en clase.

"""

__author__ = 'Escribe aquí tu nombre'

import nreinas
import random
import time


class Genetico:
    """
    Clase genérica para un algoritmo genético.
    Contiene el algoritmo genético general y las clases abstractas.

    """

    def busqueda(self, problema, n_poblacion=10, n_generaciones=30, elitismo=True):
        """
        Algoritmo genético general

        @param problema: Un objeto de la clase blocal.problema
        @param n_poblacion: Entero con el tamaño de la población
        @param n_generaciones: Número de generaciones a simular
        @param elitismo: Booleano, para aplicar o no el elitismo

        @return: Un estado del problema

        """
        poblacion = [problema.estado_aleatorio() for _ in range(n_poblacion)]

        for _ in range(n_generaciones):

            aptitud = [self.calcula_aptitud(individuo, problema.costo) for individuo in poblacion]

            elite = min(poblacion, key=problema.costo) if elitismo else None

            padres, madres = self.seleccion(poblacion, aptitud)

            poblacion = self.mutacion(self.cruza_listas(padres, madres))

            poblacion = poblacion[:n_poblacion]

            if elitismo:
                poblacion.append(elite)

        e = min(poblacion, key=problema.costo)
        return e

    def calcula_aptitud(self, individuo, costo=None):
        """
        Calcula la adaptación de un individuo al medio, mientras más adaptado mejor, por default
        es inversamente proporcionl al costo (mayor costo, menor adaptción).

        @param individuo: Un estado el problema
        @param costo: Una función de costo (recibe un estado y devuelve un número)

        @return un número con la adaptación del individuo
        """
        #return max(0, len(individuo) - costo(individuo))
        return 1.0 / (1.0 + costo(individuo))

    def seleccion(self, poblacion, aptitud):
        """
        Seleccion de estados

        @param poblacion: Una lista de individuos

        @return: Dos listas, una con los padres y otra con las madres.
        estas listas tienen una dimensión int(len(poblacion)/2)

        """
        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")

    def cruza_listas(self, padres, madres):
        """
        Cruza una lista de padres con una lista de madres, cada pareja da dos hijos

        @param padres: Una lista de individuos
        @param madres: Una lista de individuos

        @return: Una lista de individuos

        """
        hijos = []
        for (padre, madre) in zip(padres, madres):
            hijos.extend(self.cruza(padre, madre))
        return hijos

    def cruza(self, padre, madre):
        """
        Cruza a un padre con una madre y devuelve una lista de hijos, mínimo 2
        """
        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")

    def mutacion(self, poblacion):
        """
        Mutación de una población. Devuelve una población mutada

        """
        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")


class GeneticoPermutaciones1(Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """
    def __init__(self, prob_muta=0.01):
        """
        @param prob_muta : Probabilidad de mutación de un cromosoma (0.01 por defualt)

        """
        self.prob_muta = prob_muta
        self.nombre = 'propuesto por el profesor con prob. de mutación ' + str(prob_muta)

    def seleccion(self, poblacion, aptitud):
        """
        Selección por torneo.


        """
        padres = []
        baraja = range(len(poblacion))
        random.shuffle(baraja)
        for (ind1, ind2) in [(baraja[i], baraja[i+1]) for i in range(0, len(poblacion)-1, 2)]:
            ganador = ind1 if aptitud[ind1] > aptitud[ind2] else ind2
            padres.append(poblacion[ganador])

        madres = []
        random.shuffle(baraja)
        for (ind1, ind2) in [(baraja[i], baraja[i+1]) for i in range(0, len(poblacion)-1, 2)]:
            ganador = ind1 if aptitud[ind1] > aptitud[ind2] else ind2
            madres.append(poblacion[ganador])

        return padres, madres

    def cruza(self, padre, madre):
        """
        Cruza especial para problemas de permutaciones

        @param padre: Una tupla con un individuo
        @param madre: Una tupla con otro individuo

        @return: Dos individuos resultado de cruzar padre y madre con permutaciones

        """
        hijo1, hijo2 = list(padre), list(madre)
        corte1 = random.randint(0, len(padre)-1)
        corte2 = random.randint(corte1+1, len(padre))
        for i in range(len(padre)):
            if i < corte1 or i >= corte2:
                hijo1[i], hijo2[i] = hijo2[i], hijo1[i]
                while hijo1[i] in padre[corte1:corte2]:
                    hijo1[i] = madre[padre.index(hijo1[i])]
                while hijo2[i] in madre[corte1:corte2]:
                    hijo2[i] = padre[madre.index(hijo2[i])]
        return [tuple(hijo1), tuple(hijo2)]

    def mutacion(self, poblacion):
        """
        Mutación para individus con permutaciones. Utiliza la variable local self.prob_muta

        @param poblacion: Una lista de individuos (tuplas).

        @return: Los individuos mutados

        """
        poblacion_mutada = []
        for individuo in poblacion:
            individuo = list(individuo)
            for i in range(len(individuo)):
                if random.random() < self.prob_muta:
                    k = random.randint(0, len(individuo) - 1)
                    individuo[i], individuo[k] = individuo[k], individuo[i]
            poblacion_mutada.append(tuple(individuo))
        return poblacion_mutada


################################################################################################
#  AQUI EMPIEZA LO QUE HAY QUE HACER CON LA TAREA
################################################################################################

class GeneticoPermutaciones2(Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """
    def __init__(self):
        """
        Aqui puedes poner algunos de los parámetros que quieras utilizar en tu clase

        """
        self.nombre = 'propuesto por el alumno'
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------------------------------------------
        #

    def calcula_aptitud(self, individuo, costo=None):
        """
        Desarrolla un método específico de medición de aptitud.

        """
        ####################################################################
        #                          20 PUNTOS
        ####################################################################
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO --------------------------------
        #
        raise NotImplementedError("¡Este metodo debe ser implementado!")

    def seleccion(self, poblacion, aptitud):
        """
        Desarrolla un método específico de selección.

        """
        #####################################################################
        #                          20 PUNTOS
        #####################################################################
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ----------------------------------
        #
        raise NotImplementedError("¡Este metodo debe ser implementado!")

    def cruza(self, padre, madre):
        """
        Cruza especial para problemas de permutaciones

        @param padre: Una tupla con un individuo
        @param madre: Una tupla con otro individuo

        @return: Dos individuos resultado de cruzar padre y madre con permutaciones

        """
        hijo1, hijo2 = list(padre), list(madre)
        corte1 = random.randint(0, len(padre)-1)
        corte2 = random.randint(corte1+1, len(padre))
        for i in range(len(padre)):
            if i < corte1 or i >= corte2:
                hijo1[i], hijo2[i] = hijo2[i], hijo1[i]
                while hijo1[i] in padre[corte1:corte2]:
                    hijo1[i] = madre[padre.index(hijo1[i])]
                while hijo2[i] in madre[corte1:corte2]:
                    hijo2[i] = padre[madre.index(hijo2[i])]
        return [tuple(hijo1), tuple(hijo2)]

    def mutacion(self, poblacion):
        """
        Desarrolla un método específico de mutación.

        """
        ###################################################################
        #                          20 PUNTOS
        ###################################################################
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO --------------------------------
        #
        raise NotImplementedError("¡Este metodo debe ser implementado!")


def prueba_genetico_nreinas(algo_genetico, problema, n_poblacion, n_generaciones):
    tiempo_inicial = time.time()
    solucion = algo_genetico.busqueda(problema, n_poblacion, n_generaciones, elitismo=True)
    tiempo_final = time.time()
    print "\nUtilizando el algoritmo genético " + algo_genetico.nombre
    print "Con poblacion de dimensión ", n_poblacion
    print "Con ", str(n_generaciones), " generaciones"
    print "Costo de la solución encontrada: ", problema.costo(solucion)
    print "Tiempo de ejecución en segundos: ", tiempo_final - tiempo_inicial
    return solucion


if __name__ == "__main__":

    #################################################################################################
    #                          20 PUNTOS
    #################################################################################################
    # Modifica los valores de la función siguiente (o el parámetro del algo_genetico)
    # buscando que el algoritmo encuentre SIEMPRE una solución óptima, utilizando el menor tiempo
    # posible en promedio. Realiza esto para las 8, 16 y 32 reinas.
    #   -- ¿Cuales son en cada caso los mejores valores (escribelos abajo de esta lines)
    #
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun tu experiencia
    #

    solucion = prueba_genetico_nreinas(algo_genetico=GeneticoPermutaciones1(0.05),
                                       problema=nreinas.ProblemaNreinas(16),
                                       n_poblacion=32,
                                       n_generaciones=100)
    print solucion

    #################################################################################################
    #                          20 PUNTOS
    #################################################################################################
    # Modifica los valores de la función siguiente (o los posibles parámetro del algo_genetico)
    # buscando que el algoritmo encuentre SIEMPRE una solución óptima, utilizando el menor tiempo
    # posible en promedio. Realiza esto para las 8, 16 y 32 reinas.
    #   -- ¿Cuales son en cada caso los mejores valores (escribelos abajo de esta lines)
    #
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun tu experiencia? Escribelo aqui
    #   abajo, utilizando tnto espacio como consideres necesario.
    #
    # Recuerda de quitar los comentarios de las lineas siguientes:

    # solucion = prueba_genetico_nreinas(algo_genetico=GeneticoPermutaciones2(),
    #                                        problema=nreinas.ProblemaNreinas(16),
    #                                        n_poblacion=32,
    #                                        n_generaciones=500)
    # print solucion