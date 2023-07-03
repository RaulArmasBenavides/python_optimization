from pulp import *
#top 9200 
#b 1800
#INPUTS
# Datos del problema
transacciones_por_semana = 9000
transacciones_por_hora = 18
can_trans_max_hora = 20  #transaccioens
horas_por_dia = 16 #horas


#ADMINISTRADOR NO ENTRA AL MODELO
Cantidad_semana_ADM = 54  #horas
Trabajo_ADM_semanal = Cantidad_semana_ADM * transacciones_por_hora #horas
print("El admin realiza a la semana ", Trabajo_ADM_semanal) #transacciones
#no consideramos el trabajo fijo del admin
transacciones_por_semana = transacciones_por_semana - Trabajo_ADM_semanal

print("transacciones por trabajar trabajar ", transacciones_por_semana)
#cantidad máxima de trabajadores por hora
#MaxCantTrabaXHora = (can_trans_max_hora /transacciones_por_hora)+1

# Crear el problema de minimización
prob = LpProblem("Optimización de trabajadores", LpMinimize)

# Variables de decisión
dias = range(1, 8)  # Días de la semana (1 a 7)
horas = range(7, 24)  # Horas del día (7 a 23 horas)
trabajadores = ['FT', 'PT', 'PK']  # Tipos de trabajadores
variables = LpVariable.dicts("workers", (dias, horas, trabajadores), 0, 1, LpInteger)

# Función objetivo
prob +=  lpSum(variables[d][h][t] for d in dias for h in horas for t in trabajadores)

# Restricciones de capacidad
for d in dias:
    for h in horas:
        prob += lpSum(variables[d][h][t] for t in trabajadores) <= 3

# Restricciones de horario
for d in dias:
    prob += variables[d][7]['FT'] == 1  # A las 7 am debe haber un full time
    prob += lpSum(variables[d][22][t] for t in trabajadores) >= 2  # En el cierre a las 11 pm deben haber al menos 2 colaboradores

# Restricciones de horas de trabajo de cada tipo de trabajador
prob += lpSum(variables[d][h]['FT'] for d in dias) == 48
prob += lpSum(variables[d][h]['PT'] for d in dias) == 20  # El trabajador part time trabaja 20 horas a la semana
prob += lpSum(variables[d][h]['PK'] for d in dias) == 18  # El trabajador part time trabaja 20 horas a la semana
# Restricciones de demanda
 
for d in dias:
    for h in horas:
       prob += lpSum(variables[d][h][t] for t in trabajadores) >= transacciones_por_hora / transacciones_por_semana

# Restricción de máximo 1 FT y 1 PK que se turnan los días
prob += lpSum(variables[d][h]['PT'] for d in dias ) <= 1  # Máximo 1 Part Time en la semana
prob += lpSum(variables[d][h]['PK'] for d in dias ) <= 1  # Máximo 1 Pick Time en la semana


# Resolver el problema
prob.solve()

# Imprimir resultado
# print("Status:", LpStatus[prob.status])
# print("Número mínimo de trabajadores necesarios:", value(prob.objective))

# Calcular cantidad de trabajadores por categoría en la semana
count_FT = sum(value(variables[d][h]['FT']) for d in dias )
count_PT = sum(value(variables[d][h]['PT']) for d in dias )
count_PK = sum(value(variables[d][h]['PK']) for d in dias )
print("totaal ft Time:", count_FT)
print("totaal pt Time:", count_PT)
print("totaal pk Time:", count_PK)
# Imprimir cantidad de trabajadores por categoría en la semana
print("\n LINDCORP  Cantidad de trabajadores necesarios por categoría en la semana:")
print("Full Time:", count_FT/7)
print("Part Time:", count_PT/7)
print("Pick Time:", count_PK/7)