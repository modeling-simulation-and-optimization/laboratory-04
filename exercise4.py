"""
    Laboratorio 4 - MOS
    Ejercicio 4

    Realizado por:
    Juan Andrés Romero C - 202013449
    Juan Sebastián Alegría - 202011282
"""

from pyomo.environ import *
from pyomo.opt import SolverFactory
from math import sqrt
import matplotlib.pyplot as plt

model = ConcreteModel()
model.i = {'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7'}

model.coords = {'coordX', 'coordY'}
model.positions = Param(model.i, model.coords, mutable=True)

model.positions['i1', 'coordX'] = 20
model.positions['i1', 'coordY'] = 6
model.positions['i2', 'coordX'] = 22
model.positions['i2', 'coordY'] = 1
model.positions['i3', 'coordX'] = 9
model.positions['i3', 'coordY'] = 2
model.positions['i4', 'coordX'] = 3
model.positions['i4', 'coordY'] = 25
model.positions['i5', 'coordX'] = 21
model.positions['i5', 'coordY'] = 10
model.positions['i6', 'coordX'] = 29
model.positions['i6', 'coordY'] = 2
model.positions['i7', 'coordX'] = 14
model.positions['i7', 'coordY'] = 12

model.distance = Param(model.i, model.i, mutable=True)
model.graph = Param(model.i, model.i, mutable=True)

for i in model.i:
    for j in model.i:
        model.distance[i,j] = sqrt((value(model.positions[i, 'coordX'])-value(model.positions[j, 'coordX']))**2 + (value(model.positions[i, 'coordY'])-value(model.positions[j, 'coordY']))**2)
        if value(model.distance[i,j] <= 20) and value(model.distance[i,j] > 0):
            model.graph[i,j] = model.distance[i,j]
        else:
            model.graph[i,j] = 999

SOURCE_NODE = 'i4'
DESTINATION_NODE = 'i6'

# Binary variable to determine if the node is chosen or not
model.x = Var(model.i, model.i, domain=Binary)

# Target Function
model.targetFunc = Objective(expr = sum(model.graph[i, j]*model.x[i,j] for i in model.i for j in model.i), sense=minimize)

def source_node_restriction(model, i):
    if i == SOURCE_NODE:
        return sum(model.x[i,j] for j in model.i) == 1
    return Constraint.Skip

def destination_node_restriction(model, j):
    if j == DESTINATION_NODE:
        return sum(model.x[i,j] for i in model.i) == 1
    return Constraint.Skip

def intermediate_node_restriction(model, i):
    if i != SOURCE_NODE and i != DESTINATION_NODE:
        return sum(model.x[i,j] for j in model.i) - sum(model.x[j,i] for j in model.i) == 0
    return Constraint.Skip

model.source_node_restriction = Constraint(model.i, rule=source_node_restriction)
model.destination_node_restriction = Constraint(model.i, rule=destination_node_restriction)
model.intermediate_node_restriction = Constraint(model.i, rule=intermediate_node_restriction)

SolverFactory('glpk').solve(model)
model.display()


# Plot the resutling graph
plt.figure(figsize=(6,6))
plt.title('Exercise 4 - MOS')
plt.style.use('ggplot')

for i in model.i:
    for j in model.i:
        if value(value(model.graph[i,j]) != 999):
            plt.plot([value(model.positions[i, 'coordX']), value(model.positions[j, 'coordX'])], [value(model.positions[i, 'coordY']), value(model.positions[j, 'coordY'])], 'b--', dashes=(4,8))
        plt.plot(value(model.positions[i, 'coordX']), value(model.positions[i, 'coordY']), 'ro')
        plt.text(value(model.positions[i, 'coordX'])+0.5, value(model.positions[i, 'coordY'])+0.5, i, fontsize=10)

for i in model.i:
    for j in model.i:
        if value(model.x[i,j]) == 1:
            plt.plot([value(model.positions[i, 'coordX']), value(model.positions[j, 'coordX'])], [value(model.positions[i, 'coordY']), value(model.positions[j, 'coordY'])], 'r-')
plt.show()