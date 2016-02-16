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
        self.poblacion.sort(key=self.calcula_aptitud, reverse=True)
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

    @staticmethod
    def estado_a_cadena(estado):
        """
        Convierte un estado a una cadena de cromosomas

        @param estado: Una tupla con un estado
        @return: Una lista con una cadena de caracteres

        Por default converte el estado en una lista.

        """
        return list(estado)

    @staticmethod
    def cadena_a_estado(cadena):
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

        Por default usa 1 / (costo(estado) + 1)
        """
        return 1 / (1.0 +self.problema.costo(self.cadena_a_estado(individuo)))

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
        return [self.cruza_individual(self.poblacion[i][:],
                                      self.poblacion[j][:])
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
        self.prob_muta = prob_muta
        self.nombre = 'propuesto por el profesor ' \
                      'con prob. de mutación ' + str(prob_muta)
        Genetico.__init__(self, problema, n_poblacion)

    @staticmethod
    def ruleta(aptitudes):
        """
        Regresa un indice de acuerdo a la lista de aptitudes, las cuales son números >= 0

        @param aptitudes: Una lista de flotantes o enteros positivos
        @return: El indice donde podríamos decidir en forma aleatoria quedarnos

        """
        aleatorio = random.random()
        acumulado = 0
        suma_aptitudes = 1.0 * sum(aptitudes)
        for (i, aptitud) in enumerate(aptitudes):
            acumulado += aptitud / suma_aptitudes
            if aleatorio <= acumulado:
                return i
        raise ValueError("No debe pasar esto")

    def seleccion_individual(self):
        """
        Realiza una única pareja por medio de la ruleta

        @return: Una tupla con los pares a unirse

        """
        i = self.ruleta(self.aptitud[:])
        j = self.ruleta(self.aptitud[:i] + self.aptitud[i+1:])
        return i, j if j < i else j+1

    def seleccion(self):
        """
        Selección por ruleta.

        """
        return [self.seleccion_individual()
                for _ in range(self.n_poblacion)]

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza especial para problemas de permutaciones

        @param cadena1: Una tupla con un individuo
        @param cadena2: Una tupla con otro individuo
        @return: Un individuo

        """
        hijo = cadena1[:]
        len_cadena = len(hijo)
        corte1 = random.randint(0, len_cadena - 1)
        corte2 = random.randint(corte1 + 1, len_cadena)
        evita = hijo[:corte1] + hijo[corte2:]
        for i in range(corte1, corte2):
            hijo[i] = cadena2[i]
            while hijo[i] in evita:
                hijo[i] = cadena2[cadena1.index(hijo[i])]
        return hijo

    def mutacion(self, poblacion):
        """
        Mutación para individus con permutaciones.
        Utiliza la variable local self.prob_muta

        @param poblacion: Una lista de individuos (tuplas).

        @return: Los individuos mutados

        """
        for individuo in poblacion:
            for i in range(len(individuo)):
                if random.random() < self.prob_muta:
                    k = random.randint(0, len(individuo) - 1)
                    individuo[i], individuo[k] = individuo[k], individuo[i]


################################################################################################
#  AQUI EMPIEZA LO QUE HAY QUE HACER CON LA TAREA
#
# Básicamente, hacer un algoritmo genético completo y diferente
################################################################################################

class GeneticoPermutaciones2(Genetico):
    """
    Clase con un algoritmo genético adaptado a problemas de permutaciones

    """
    def __init__(self):
        """
        Aqui puedes poner algunos de los parámetros
        que quieras utilizar en tu clase

        Recuerda que puedes cambiar la forma de representación para que
        se puedan utilizar operadores clásicos (esto implica reescribir
        los métodos estáticos cadea_a_estado y estado_a_cadena).

        """
        self.nombre = 'propuesto por el alumno'
        Genetico.__init__(self, problema, n_poblacion)
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO -----------------------------------
        #

    def calcula_aptitud(self, individuo):
        """
        Calcula la adaptación de un individuo al medio, mientras más adaptado
        mejor, mayor costo, menor adaptción.

        @param individuo: Una lista de cromosomas
        @return un número con la adaptación del individuo

        """
        ####################################################################
        #                          10 PUNTOS
        ####################################################################
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO --------------------------------
        #
        raise NotImplementedError("¡Este metodo debe ser implementado!")

    def seleccion(self):
        """
        Seleccion de estados

        @return: Una lista con pares de indices de los individuo que se van
                 a cruzar

        """
        #####################################################################
        #                          10 PUNTOS
        #####################################################################
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ----------------------------------
        #
        raise NotImplementedError("¡Este metodo debe ser implementado!")

    def cruza_individual(self, cadena1, cadena2):
        """
        Cruza dos individuos representados por sus cadenas

        @param cadena1: Una lista de cromosomas
        @param cadena2: Una lista de cromosomas

        @return: Un individuo nuevo

        """
        #####################################################################
        #                          10 PUNTOS
        #####################################################################
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ----------------------------------
        #
        raise NotImplementedError("¡Este metodo debe ser implementado!")

    def mutacion(self, poblacion):
        """
        Mutación para individuos con permutaciones.
        Utiliza la variable local self.prob_muta

        @param poblacion: Una lista de individuos (tuplas).

        @return: Los individuos mutados

        """
        ###################################################################
        #                          10 PUNTOS
        ###################################################################
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO --------------------------------
        #
        raise NotImplementedError("¡Este metodo debe ser implementado!")

    def reemplazo(self, hijos):
        """
        Realiza el reemplazo generacional

        @param hijos: Una lista de cromosomas de hijos que pueden usarse en el
                      reemplazo
        @return: None (todo lo cambia internamente)

        Por default usamos solo el elitismo de conservar al mejor, solo si es
        mejor que lo que hemos encontrado hasta el momento.

        """
        ###################################################################
        #                          10 PUNTOS
        ###################################################################
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO --------------------------------
        #


class ProblemaTonto(object):
    """
    Clase de problema tonto, solo para pruebas visuales

    El costo es la suma del primer y último valor

    """
    def __init__(self, n):
        self.n = n

    def estado_aleatorio(self):
        lista = range(self.n)
        random.shuffle(lista)
        return tuple(lista)

    def costo(selfself, estado):
        return estado[0] + estado[-1]


# Ahora vamos a mostrar una forma visual de ver si el método que están
# desarrollando tiene buena pinta o no.
#
# En general solo son algunas pruebas visuales y no puede considerarse todavía
# como una unidad de prueba ni siquiera básica. Usarlo con su propio algoritmo
# genético para evitar sorpresas.

if __name__ == "__main__":

    # Un objeto genético con permutaciones con una población de
    # 10 individuos y una probabilidad de mutacion de 0.1
    genetico = GeneticoPermutaciones1(ProblemaTonto(10), 10, 0.1)

    print "El nombre del algortimo es: ", genetico.nombre
    print "Y el conjunto de estados iniciales es: "
    for (i, cadena) in enumerate(genetico.poblacion):
        assert isinstance(cadena, list)
        print i, ': ', cadena, " aptitud = ", genetico.aptitud[i]
    print "\nPor la forma de estar programado" \
          "la aptitud debe estar en orden descendente\n"

    parejas = genetico.seleccion()
    print "Un ejemplo de parejitas sería:"
    for (i, j) in parejas:
        print "estado ", i, " se reproduce con el estado ", j
    print "\nLos mejores se espera se reproduzcan más\n"

    cadena1 = genetico.poblacion[parejas[0][0]]
    cadena2 = genetico.poblacion[parejas[0][1]]
    hijo = genetico.cruza_individual(cadena1, cadena2)
    print "Y para observar la cruza tenemos: "
    print "progenitor 1: ", cadena1
    print "progenitor 2: ", cadena2
    print "descendiente: ", hijo

    hijos = genetico.cruza(parejas)
    print "Haciendo una cruza de todas las parejas tenemos que: "
    for (i, cadena) in enumerate(hijos):
        assert isinstance(cadena, list)
        print i, ': ', cadena
    genetico.mutacion(hijos)
    print "Y después de la mutación tenemos:"
    for (i, cadena) in enumerate(hijos):
        assert isinstance(cadena, list)
        print i, ': ', cadena

    mejor = genetico.busqueda(30)
    print "\n\nSi iteramos por 30 generaciones tenemos que\n" \
          "el estado que encontramos con menor costo es:\n"
    print mejor
    print "\nQue debería tener el 0 y el 1 a los extremos"


