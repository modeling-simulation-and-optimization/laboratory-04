"""
Laboratorio 4 - MOS
Ejercicio 2

Realizado por:
Juan Andrés Romero C - 202013449
Juan Sebastián Alegría - 202011282
"""

from pyomo.environ import *
from pyomo.opt import SolverFactory

model = ConcreteModel()

# Sets and parameters
model.i = {'i1', 'i2', 'i3', 'i4', 'i5', 'i6'}  # Town sets

# Distance between towns
model.distance = Param(model.i, model.i, mutable=True)

for i in model.i:
    for j in model.i:
        model.distance[i, j] = 0

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

        if (value(model.distance[i, j]) <= 15 and value(model.distance[i, j]) >= 1) or (value(model.distance[j, i]) <= 15 and value(model.distance[j, i]) >= 1):
            model.distance[i, j] = 1
            model.distance[j, i] = 1
        else:
            model.distance[i, j] = 0
            model.distance[j, i] = 0

# Variables
# Binary variable to determine if town is chosen or not
model.x = Var(model.i, domain=Binary)

# Objective function
model.targetFunc = Objective(expr=sum(model.x[i] for i in model.i), sense=minimize)  # Target Function


# Constraints
def min_zones(model, i):
    return sum(model.x[j]*model.distance[i, j] for j in model.i) >= 1


model.min_zones = Constraint(model.i, rule=min_zones)

# Applying the solver
SolverFactory('glpk').solve(model)
model.display()
