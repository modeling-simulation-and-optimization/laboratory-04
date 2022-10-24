"""
    Laboratorio 4 - MOS
    Ejercicio 2

    Realizado por:
    Juan Andrés Romero C - 202013449
    Juan Sebastián Alegría - 202011282
"""

from pyomo.environ import ConcreteModel, Param, Var, Objective, value, minimize, Binary, Constraint
from pyomo.opt import SolverFactory

model = ConcreteModel()
# Town sets
model.i = {'i1', 'i2', 'i3', 'i4', 'i5', 'i6'}

# Distance between towns
model.distance = Param(model.i, model.i, mutable=True)

for i in model.i:
    for j in model.i:
        model.distance[i,j] = 0

model.distance['i1', 'i2'] = 10
model.distance['i1', 'i3'] = 20
model.distance['i1', 'i4'] = 30
model.distance['i1', 'i5'] = 30
model.distance['i1', 'i6'] = 20

model.distance['i2', 'i3'] = 25
model.distance['i2', 'i4'] = 35
model.distance['i2', 'i5'] = 20
model.distance['i2', 'i6'] = 10

model.distance['i3', 'i4'] = 15
model.distance['i3', 'i5'] = 30
model.distance['i3', 'i6'] = 20

model.distance['i4', 'i5'] = 15
model.distance['i4', 'i6'] = 25

model.distance['i5', 'i6'] = 14

for i in model.i:
    for j in model.i:
        if value(model.distance[i, j]) != 0:
            model.distance[j, i] = model.distance[i, j]

        if (value(model.distance[i, j]) <= 15 and value(model.distance[i,j])>=1) or (value(model.distance[j,i]) <= 15 and value(model.distance[j,i]) >=1):
            model.distance[i,j] = 1
        else:
            model.distance[i,j] = 0

        if value(model.distance[i, j]) != 0:
            model.distance[j,i] = model.distance[i, j]

model.x = Var(model.i, domain=Binary) # Binary variable to determine if town is chosen or not

model.targetFunc = Objective(expr= sum(model.x[i] for i in model.i), sense=minimize) # Target Function

def min_zones(model, i):
    return sum(model.x[j]*model.distance[i,j] for j in model.i) >= 1

model.minZones = Constraint(model.i, rule=min_zones)

SolverFactory('glpk').solve(model)
model.display()