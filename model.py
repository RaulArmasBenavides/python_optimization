# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 22:55:14 2023

@author: raula
"""
# cargar la librería PuLP
from pulp import *
# Problema de programación lineal
prob = LpProblem("test_de_optimizacion", LpMinimize)
# Variables
# 0 <= x <= 4
x = pulp.LpVariable("x", 0, 4)
# -1 <= y <= 1
y = pulp.LpVariable("y", -1, 1)
# Objetivo
prob += x + 4*y, "obj"

# Restricciones
prob += x+y <= 5, "c1"

prob.solve()
# Impresión de los valores de las variables óptimas
for v in prob.variables():
  print(v.name, "=", v.varValue)
  # Valor objetivo
  print("objective=", value(prob.objective))