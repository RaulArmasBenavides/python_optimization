# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 21:57:35 2023

@author: raula
"""
from pulp import *
# Crear el problema
prob = LpProblem("Ejemplo_Problema", LpMinimize)

# Variables de decisión
x = LpVariable("x", lowBound=0)  # Variable x no negativa
y = LpVariable("y", lowBound=0)  # Variable y no negativa
# Función objetivo
prob += 3 * x + 5 * y , "obj"
# Restricciones
prob += 2 * x + y >= 10, "c1"
prob += x + 3 * y >= 12, "c2"

# Resolver el problema
prob.solve()

# Imprimir el estado de la solución
print("Estado:", LpStatus[prob.status])

# Imprimir los valores de las variables óptimas
print("Valor óptimo de x:", value(x))
print("Valor óptimo de y:", value(y))

# Imprimir el valor óptimo de la función objetivo
print("Valor óptimo de la función objetivo:", value(prob.objective))
