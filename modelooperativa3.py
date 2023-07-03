from pulp import *

# Parámetros
T =  1800# Número total de transacciones en una semana
FT_WORK_HOURS = 8
PT_WORK_HOURS = 4
PK_WORK_HOURS = 6
MAX_WORKERS = 3
MIN_WORKERS = 4
MAX_FT = 6
MAX_PT = 1
MAX_PK = 1
Days = range(1, 8)  # Días de la semana
Weeks = range(1, 2)  # Semanas

# Crear el problema de optimización
prob = LpProblem("Optimización de trabajadores", LpMinimize)

# Variables de decisión
FT = LpVariable.dicts("FT", (Days, Weeks), lowBound=0, cat='Integer')
PT = LpVariable.dicts("PT", (Days, Weeks), lowBound=0, cat='Integer')
PK = LpVariable.dicts("PK", (Days, Weeks), lowBound=0, cat='Integer')

# Función objetivo
prob += lpSum(FT[i][j] + PT[i][j] + PK[i][j] for i in Days for j in Weeks)

# Restricciones de horas de trabajo
prob += lpSum(FT[i][j] * FT_WORK_HOURS + PT[i][j] * PT_WORK_HOURS + PK[i][j] * PK_WORK_HOURS for i in Days for j in Weeks) == T * 18

# Restricciones de horarios
prob += FT[1][j] >= 1 for j in Weeks
prob += FT[7][j] + PT[7][j] + PK[7][j] >= 2 for j in Weeks

# Restricción de número máximo de trabajadores
for i in Days:
    for j in Weeks:
        prob += FT[i][j] + PT[i][j] + PK[i][j] <= MAX_WORKERS

# Restricciones de número máximo de empleados por categoría en la semana
prob += lpSum(FT[i][j] for i in Days for j in Weeks) <= MAX_FT
prob += lpSum(PT[i][j] for i in Days for j in Weeks) <= MAX_PT
prob += lpSum(PK[i][j] for i in Days for j in Weeks) <= MAX_PK

# Restricción de número mínimo de trabajadores en la tienda por día
for i in Days:
    for j in Weeks:
        prob += FT[i][j] + PT[i][j] + PK[i][j] >= MIN_WORKERS

# Restricción de máximo 1 empleado part time y 1 empleado pick time en la semana
prob += lpSum(PT[i][j] for i in Days for j in Weeks) <= 1
prob += lpSum(PK[i][j] for i in Days for j in Weeks) <= 1

# Resolver el problema
prob.solve()

# Imprimir la solución
print("Estado:", LpStatus[prob.status])
print("Número mínimo de trabajadores:", value(prob.objective))

# Imprimir la asignación de trabajadores
for i in Days:
    for j in Weeks:
        print("Día", i, "Semana", j)
        print("Full time:", value(FT[i][j]))
        print("Part time:", value(PT[i][j]))
        print("Pick time:", value(PK[i][j]))
        print()