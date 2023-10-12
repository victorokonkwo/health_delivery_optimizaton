
from pyomo.environ import *
import random
# Define your model
model = ConcreteModel()

# Define the set of staff members (i) and time slots (t)
N = range(1, 21) # N (1-21)
T = range(1, 11)  # T (1-11)

# Define the binary decision variables xit for each i and t
model.x = Var(N, T, within=Binary)

# Define the demand for staff at each time slot (Dt) within the range 1-10
def Dt_init(model, t):
    return random.randint(1, 10)

model.Dt = Param(T, initialize=Dt_init) # Replace '...' with the demand for each time slot (1-10)

# Define the constraint
def demand_constraint_rule(model, t):
    return sum(model.x[i, t] for i in N) == model.Dt[t]

model.demand_constraint = Constraint(T, rule=demand_constraint_rule)


# Define the binary decision variables xit for each i and t


# Define the parameter Hi for the upper bound
def H_init(model, i):
    return random.randint(8, 12)

model.H = Param(N, initialize=H_init)
# Define the upper bound constraint using the LaTeX representation
def upper_bound_constraint_rule(model, i):
    return sum(model.x[i, t] for t in T) <= model.H[i]

model.upper_bound_constraint = Constraint(N, rule=upper_bound_constraint_rule)

# Define the sets T and P
P = range(1,31)  # Replace '...' with the range of values for P

# Define the decision variables ypt for each t and p
model.y = Var(T, P, within=Binary)


# Define the constraint
def summation_constraint_rule(model, p):
    return sum(model.y[t, p] for t in T) == 1

model.summation_constraint = Constraint(P, rule=summation_constraint_rule)


R = range(1, 11)  # Replace '...' with the number of R values

# Define the decision variable z
model.z = Var(R, T, within=Binary)

# Define the constraint
def resource_constraint_rule(model, r):
    return sum(model.z[r, t] for t in T) == 1

model.resource_constraint = Constraint(R, rule=resource_constraint_rule)


model.o = Var(N, within=Binary)

# Define the constraint
def overtime_rule(model, i):
    return model.o[i] >= sum(model.x[i, t] for t in T) - model.H[i]

model.overtime = Constraint(N, rule=overtime_rule)


# Define the parameter W with random integer values between 1 and 10
def W_init(model, i, t):
    return random.randint(1, 10)

model.W = Param(N, T, initialize=W_init)


def O_init(model, i):
    return random.randint(1, 10)

model.O = Param(N, initialize=O_init)


def D_init(model, r, t):
    return random.randint(2, 5)

model.D = Param(R, T, initialize=D_init)

# Define parameters and decision variables as needed.

# Define the constraint
model.budget = Constraint(
    expr=sum(model.W[i, t] * model.x[i, t] + model.O[i] * model.o[i] for i in N for t in T) +
          sum(model.D[r, t] * model.z[r, t] for r in R for t in T) <= 20
)


K = range(1, 16)
# Define the S values for each staff member
  # Replace '...' with the values of S for each staff member

def S_init(model, n):
    return random.randint(1, 5)

model.S = Param(N, initialize=S_init)
# Define the M values for each i, p, k, and t
# M = {(i, p, k, t) : (i, p, k, t)
#      for i in N for p in P for k in K for t in T}  

def M_init(model, n, p, k, t):
    return random.randint(1, 5)

model.M = Param(N, P, K, T, initialize=M_init)

# Define the constraint
# Define the constraint using expr

def constraint_expr_rule(model, n, p, k, t):
    return sum(model.x[i, t] * model.S[i] for i in N) >= model.M[n, p, k, t]

model.skill = Constraint(N, P, K, T, rule=constraint_expr_rule)

def F_init(model, i, j):
    return random.randint(1, 3)

model.F = Param(N, N, initialize=F_init)

# Define the constraint
def max_difference_constraint_rule(model, i, j):
    if i != j:
        return sum(model.x[i, t] for t in T) - sum(model.x[j, t] for t in T) <= model.F[i, j]
    else:
        return Constraint.Skip

model.max_difference_constraint = Constraint(N, N, rule=max_difference_constraint_rule)

# You can add additional constraints and objective functions as needed.

def I_init(model, i, j, t):
    return random.randint(1, 10)

model.I = Param(N, N, T, initialize=I_init)

def P_init(model, p, t):
    return random.randint(1, 10)

model.P = Param(P,  T, initialize=P_init)

def U_init(model, p):
    return random.randint(1, 10)

model.U = Param(P, initialize=U_init)


def C_init(model, p, t):
    return random.randint(1, 10)

model.C = Param(P, T, initialize=C_init)

model.v = Var(N, P, within=Binary)

def objective_rule(model):
    return (sum(model.W[i, t] * model.x[i, t] for i in N for t in T) + 
            sum(model.I[i, j, t] * model.x[i, t] * model.x[j, t] for i in N for j in N for t in T) +
            sum(model.C[p, t] * model.y[t, p] for p in P for t in T) +
            sum(model.D[r, t] * model.z[r, t] for r in R for t in T) +
            sum(model.P[p, t] * model.y[t, p] for p in P for t in T) +
            sum(model.O[i] * model.o[i] for i in N) +
            sum(model.U[p] * model.v[i, p] for p in P for i in N for k in K for t in T) +
            sum(model.S[i] * model.x[i, t] for i in N for t in T)
        )

model.objective = Objective(rule=objective_rule, sense=minimize)

opt = SolverFactory("gurobi", solver_io="python")


opt.solve(model)

model.pprint()