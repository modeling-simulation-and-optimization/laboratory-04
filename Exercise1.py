"""
    Laboratorio 4 - MOS
    Ejercicio 1

    Realizado por:
    Juan Andrés Romero C - 202013449
    Juan Sebastián Alegría - 202011282
"""

from pyomo.environ import *
from pyomo.opt import SolverFactory

model = ConcreteModel()

model.i = {'i1', 'i2', 'i3'} # Origin CPUs
model.j = {'j1', 'j2'} # Destination CPUs
model.p = {'pk', 'pu'} # Process types

model.oProcess = Param(model.i, model.p, mutable=True) # Amount of processes supplied by origin
model.dProcess = Param(model.j, model.p, mutable=True) # Amount of processes demanded by destination
model.cost = Param(model.i, model.j, mutable=True) # Cost of sending processes from origin to destination

model.oProcess['i1', 'pk'] = 60
model.oProcess['i1', 'pu'] = 80
model.oProcess['i2', 'pk'] = 80
model.oProcess['i2', 'pu'] = 50
model.oProcess['i3', 'pk'] = 50
model.oProcess['i3', 'pu'] = 50

model.dProcess['j1', 'pk'] = 100
model.dProcess['j1', 'pu'] = 60
model.dProcess['j2', 'pk'] = 90
model.dProcess['j2', 'pu'] = 120

model.cost['i1', 'j1'] = 300
model.cost['i1', 'j2'] = 500
model.cost['i2', 'j1'] = 200
model.cost['i2', 'j2'] = 300
model.cost['i3', 'j1'] = 600
model.cost['i3', 'j2'] = 300

model.x = Var(model.i, model.j, model.p, domain=NonNegativeReals) # Amount of processes sent per path and type

model.targetFunc = Objective(expr = sum(model.cost[i, j] * model.x[i, j, p] for i in model.i for j in model.j for p in model.p), sense=minimize) # Target Function

def max_processes_sent(model, i, p):
    return sum(model.x[i, j, p] for j in model.j) <= model.oProcess[i, p]

def satisfied_CPU_demand(model, j, p):
    return sum(model.x[i, j, p] for i in model.i) == model.dProcess[j, p]

model.maxProcessesSent = Constraint(model.i, model.p, rule=max_processes_sent)
model.satisfiedCPUDemand = Constraint(model.j, model.p, rule=satisfied_CPU_demand)

SolverFactory('glpk').solve(model)
model.display()
