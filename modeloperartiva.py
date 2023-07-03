from pulp import *

# Datos del problema
transacciones_por_semana = 9000
transacciones_por_hora = 18
can_trans_max_dia = 20  #horas
horas_por_dia = 15 #horas
MaxCantTrabaXHora = (can_trans_max_dia /transacciones_por_hora)+1
# Crear el problema de minimización
prob = LpProblem("Optimización de trabajadores", LpMinimize)

# Variables de decisión
dias = range(1, 8)  # Días de la semana (1 a 7)
horas = range(7, 22)  # Horas del día (7 a 21)
trabajadores = ['FT', 'PT', 'PK', 'ADM']  # Tipos de trabajadores
variables = LpVariable.dicts("workers", (dias, horas, trabajadores), 0, 1, LpInteger)

# Función objetivo
prob += lpSum(variables[d][h][t] for d in dias for h in horas for t in trabajadores)

# Restricciones de capacidad
for d in dias:
    for h in horas:
        prob += lpSum(variables[d][h][t] for t in trabajadores) <= MaxCantTrabaXHora

# Restricciones de horario
for d in dias:
    prob += variables[d][7]['FT'] == 1  # A las 7 am debe haber un full time
    prob += lpSum(variables[d][21][t] for t in trabajadores) >= 2  # En el cierre a las 10 pm deben haber al menos 2 colaboradores

# Restricciones de disponibilidad del administrador
for d in dias:
    if d == 7:  # El administrador no trabaja los domingos
        prob += lpSum(variables[d][h]['ADM'] for h in horas) == 0
    else:
        prob += lpSum(variables[d][h]['ADM'] for h in horas) == 9  # El administrador trabaja de 9 am a 6 pm de lunes a sábado

# Restricciones de disponibilidad del trabajador part time en planilla
prob += lpSum(variables[d][h]['PT'] for d in dias for h in horas) == 20  # El trabajador part time trabaja 20 horas a la semana

# Restricciones de disponibilidad del trabajador pick time
for d in range(1, 4):
    prob += lpSum(variables[d][h]['PK'] for h in horas) == 6  # El trabajador pick time trabaja 6 horas los primeros 3 días

# Restricciones de demanda
for d in dias:
    for h in horas:
        prob += lpSum(variables[d][h][t] for t in trabajadores) >= transacciones_por_hora / transacciones_por_semana

# Resolver el problema
prob.solve()

# Imprimir resultado
print("Status:", LpStatus[prob.status])
print("Número mínimo de trabajadores necesarios:", value(prob.objective))

# Calcular cantidad de trabajadores por categoría en la semana
count_FT = sum(value(variables[d][h]['FT']) for d in dias for h in horas)
count_PT = sum(value(variables[d][h]['PT']) for d in dias for h in horas)
count_PK = sum(value(variables[d][h]['PK']) for d in dias for h in horas)

# Imprimir cantidad de trabajadores por categoría en la semana
print("\n LINDCORP  Cantidad de trabajadores necesarios por categoría en la semana:")
print("Full Time:", count_FT/7)
print("Part Time:", count_PT/7)
print("Pick Time:", count_PK/7)