from pulp import *

# Entradas/Inputs
transacciones_por_semana = 1800
transacciones_por_hora = 18
can_trans_max_hora = 20
horas_por_dia = 16

# Trabajo del administrador
Cantidad_semana_ADM = 54
Trabajo_ADM_semanal = Cantidad_semana_ADM * transacciones_por_hora
transacciones_por_semana -= Trabajo_ADM_semanal

MaxCantTrabaXHora = (can_trans_max_hora /transacciones_por_hora) + 1
print("Se tienen que atender:", transacciones_por_semana)
# Creación del problema
prob = LpProblem("Optimización de trabajadores", LpMinimize)

# Variables de decisión
dias = range(1, 8)
horas = range(7, 24)
trabajadores = ['FT', 'PT', 'PK']
variables = LpVariable.dicts("workers", (dias, horas, trabajadores), 0, 1, LpInteger)

# Función objetivo
prob += lpSum(variables[d][h][t] for d in dias for h in horas for t in trabajadores)

# Restricciones
for d in dias:
    for h in horas:
        prob += lpSum(variables[d][h][t] for t in trabajadores) <= MaxCantTrabaXHora

for d in dias:
    prob += variables[d][7]['FT'] == 1
    prob += lpSum(variables[d][22][t] for t in trabajadores) >= 2

# Removemos las restricciones absolutas de los FTs y mantenemos las de PT y PK
prob += lpSum(variables[d][h]['PT'] for d in dias) == 20
prob += lpSum(variables[d][h]['PK'] for d in dias) == 18

for d in dias:
    for h in horas:
        prob += lpSum(variables[d][h][t] for t in trabajadores) * transacciones_por_hora >= transacciones_por_semana

prob += lpSum(variables[d][h]['PT'] for d in dias) <= 1
prob += lpSum(variables[d][h]['PK'] for d in dias) <= 1

# Resolver
prob.solve()

# Imprimir resultados
print("Status:", LpStatus[prob.status])
print("Número mínimo de trabajadores necesarios para las 4 semanas:", value(prob.objective))

unique_FT = sum(1 for d in dias if sum(value(variables[d][h]['FT']) for h in horas) > 0)
unique_PT = sum(1 for d in dias if sum(value(variables[d][h]['PT']) for h in horas) > 0)
unique_PK = sum(1 for d in dias if sum(value(variables[d][h]['PK']) for h in horas) > 0)

print("Total Full Time:", unique_FT)
print("Total Part Time:", unique_PT)
print("Total Pick Time:", unique_PK)

# Estos son los trabajadores requeridos por semana (y son constantes para las 4 semanas del mes)
print("\n LINDCORP  Cantidad de trabajadores necesarios por semana (constantes para las 4 semanas del mes):")
print("Full Time:", unique_FT)
print("Part Time:", unique_PT)
print("Pick Time:", unique_PK)