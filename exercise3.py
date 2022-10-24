"""
    Laboratorio 4 - MOS
    Ejercicio 3

    Realizado por:
    Juan Andrés Romero C - 202013449
    Juan Sebastián Alegría - 202011282
"""

from pyomo.environ import *
from pyomo.opt import SolverFactory

model = ConcreteModel()

# Sets and parameters
model.t = RangeSet(1, 20)  # Tile set
model.p = RangeSet(1, 7)  # Pipes

# Establishes if said tile has or not a pipe
model.has_pipe = Param(model.t, model.p, mutable=True)

for t in model.t:
    for p in model.p:
        model.has_pipe[t, p] = 0

model.has_pipe[1, 1] = 1
model.has_pipe[5, 1] = 1

model.has_pipe[5, 2] = 1
model.has_pipe[9, 2] = 1

model.has_pipe[9, 3] = 1
model.has_pipe[10, 3] = 1
model.has_pipe[13, 3] = 1
model.has_pipe[14, 3] = 1

model.has_pipe[13, 4] = 1
model.has_pipe[17, 4] = 1

model.has_pipe[2, 5] = 1
model.has_pipe[3, 5] = 1
model.has_pipe[6, 5] = 1
model.has_pipe[7, 5] = 1

model.has_pipe[10, 6] = 1
model.has_pipe[11, 6] = 1
model.has_pipe[14, 6] = 1
model.has_pipe[15, 6] = 1

model.has_pipe[8, 7] = 1
model.has_pipe[12, 7] = 1
model.has_pipe[16, 7] = 1
model.has_pipe[20, 7] = 1
model.has_pipe[19, 7] = 1

# Variables
model.x = Var(model.t, domain=Binary)  # Node selected

# Objective function
model.obj = Objective(expr=sum(model.x[t] for t in model.t), sense=minimize)

# Constraints
model.min_tiles = ConstraintList()  # Pipe coverage rule
for p in model.p:
    model.min_tiles.add(sum(model.x[t]*model.has_pipe[t, p] for t in model.t) >= 1)

# Applying the solver
SolverFactory('glpk').solve(model)
model.display()
