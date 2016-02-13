#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
genetico.py
------------

Este modulo incluye el algoritmo genérico para algoritmos genéticos, así como un
algoritmo genético adaptado a problemas de permutaciones, como el problema de
las n-reinas o el agente viajero.

Como tarea se pide desarrollar otro algoritmo genético con el fin de probar
otro tipobde métodos internos, así como ajustar ambos algortmos para que
funcionen de la mejor manera posible.


Para que funcione, este modulo debe de encontrarse en la misma carpeta que
blocales.py y nreinas.py vistas en clase.

"""

import math
import random
import time
import nreinas

__author__ = 'Escribe aquí tu nombre'


class Genetico:
    """
    Clase genérica para un algoritmo genético.
    Contiene el algoritmo genético general y las clases abstractas.

    """

    def __init__(self, problema, n_poblacion):
        self.problema = problema
        self.inicializa_poblacion(n_poblacion)

    def inicializa_poblacion(self, n_poblacion):
        """
        Inicializa la población para el algoritmo genético

        @param n_poblacion: numero de población
        @return: None

        Internamente guarda self.npoblacion y self.poblacion

        """
        self.poblacion = [self.estado_a_cadena(self.problema.estado_aleatorio())
                          for _ in range(n_poblacion)]
        self.poblacion.sort(key=self.calcula_aptitud)
        self.n_poblacion = n_poblacion
        self.aptitud = [self.calcula_aptitud(individuo)
                        for individuo in self.poblacion]

    def busqueda(self, n_generaciones=30):
        """
        Algoritmo genético general

        @param n_generaciones: Número de generaciones a simular
        @return: Un estado del problema

        """
        for _ in range(n_generaciones):
            parejas = self.seleccion()
            hijos = self.cruza(parejas)
            self.mutacion(hijos)
            self.reemplazo(hijos)
        mas_apto = max(self.poblacion, key=self.calcula_aptitud)
        return self.cadena_a_estado(mas_apto)

    def estado_a_cadena(self, estado):
        """
        Convierte un estado a una cadena de cromosomas

        @param estado: Una tupla con un estado
        @return: Una lista con una cadena de caracteres

        Por default converte el estado en una lista.

        """
        return list(estado)

    def cadena_a_estado(self, cadena):
        """
        Convierte una cadena de cromosomas a un estado

        @param cadena: Una lista de cromosomas o valores
        @return: Una tupla con un estado válido

        Por default convierte la lista a tupla

        """
        return tuple(cadena)

    def calcula_aptitud(self, individuo):
        """
        Calcula la adaptación de un individuo al medio, mientras más adaptado
        mejor, mayor costo, menor adaptción.

        @param individuo: Una lista de cromosomas
        @return un número con la adaptación del individuo

        Por default usa exp(-costo(estado))
        """
        return math.exp(-self.problema.costo(self.cadena_a_estado(individuo)))

    def seleccion(self):
        """
        Seleccion de estados

        @return: Una lista con pares de indices de los individuo que se van
                 a cruzar

        """
        raise NotImplementedError("falta implementar la selección")

    def cruza(self, parejas):
        """
        Cruza a un padre con una madre y devuelve una lista de hijos, mínimo 2

        @param parejas: Una lista de tuplas (i,j) con los indices de los
                        individuos de self.poblacion a cruzarse
        @return Una lista de hijos (listas de cromosomas a su vez)

        """
        return [self.cruza_individual(self.poblacion[i], self.poblacion[j])
                for (i, j) in parejas]

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza dos individuos representados por sus cadenas

        @param cadena1: Una lista de cromosomas
        @param cadena2: Una lista de cromosomas

        @return: Un individuo nuevo

        """
        raise NotImplementedError("A implementar la cruza individual")

    def mutacion(self, poblacion):
        """
        Mutación de una población. Devuelve una población mutada
        la cual se pasa por referencia (variables mutables)

        @param poblacion: Una lista de listas de cromosomas

        """
        raise NotImplementedError("A implementar la mutación")

    def reemplazo(self, hijos):
        """
        Realiza el reemplazo generacional

        @param hijos: Una lista de cromosomas de hijos que pueden usarse en el
                      reemplazo
        @return: None (todo lo cambia internamente)

        Por default usamos solo el elitismo de conservar al mejor, solo si es
        mejor que lo que hemos encontrado hasta el momento.

        """
        hijos.sort(key=self.calcula_aptitud, reverse=True)
        apt_hijos = [self.calcula_aptitud(individuo) for individuo in hijos]
        if apt_hijos[0] > self.aptitud[0]:
            self.poblacion = hijos[:self.n_poblacion]
            self.aptitud = apt_hijos[:self.n_poblacion]
        else:
            self.poblacion = [self.poblacion[0]] + hijos[:self.n_poblacion - 1]
            self.aptitud = [self.aptitud[0]] + apt_hijos[:self.n_poblacion - 1]
        del(hijos)



class GeneticoPermutaciones1(Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """
    def __init__(self, problema, n_poblacion, prob_muta=0.01):
        """
        @param prob_muta : Probabilidad de mutación de un cromosoma (0.01 por defualt)

        """
        Genetico.__init__(self, problema, n_poblacion)
        self.prob_muta = prob_muta
        self.nombre = 'propuesto por el profesor ' \
                      'con prob. de mutación ' + str(prob_muta)

    def seleccion(self):
        """
        Selección por ruleta.

        """

        baraja = range(self.n_poblacion)
        random.shuffle(baraja)
        for :
            ganador = ind1 if self.aptitud[ind1] > self.aptitud[ind2] else ind2

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