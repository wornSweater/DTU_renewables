from pyomo.environ import *
from pyomo.mpec import *

# case from Lecture 2
def run_l2_mcp_inelastic():
    # 0. input of the demand amount
    while True:
        try:
            demand = float(input("Enter the demand amount: "))
            break
        except:
            print("Please enter a non-negative number.")
            continue

    # 1. create a MCP model
    model = ConcreteModel()

    # 2. define variables
    model.p_w1 = Var()
    model.p_g1 = Var()
    model.p_g2 = Var()
    model.mu_w1_lower = Var()
    model.mu_w1_upper = Var()
    model.mu_g1_lower = Var()
    model.mu_g1_upper = Var()
    model.mu_g2_lower = Var()
    model.mu_g2_upper = Var()
    model.market_price = Var()

    vars = [
        model.p_w1,
        model.p_g1,
        model.p_g2,
        model.mu_w1_lower,
        model.mu_w1_upper,
        model.mu_g1_lower,
        model.mu_g1_upper,
        model.mu_g2_lower,
        model.mu_g2_upper,
        model.market_price,
    ]

    # 3. define equalities and complementarity conditions
    model.eq1 = Constraint(expr=0 + model.mu_w1_upper - model.mu_w1_lower - model.market_price == 0)
    model.eq2 = Constraint(expr=20 + model.mu_g1_upper - model.mu_g1_lower - model.market_price == 0)
    model.eq3 = Constraint(expr=30 + model.mu_g2_upper - model.mu_g2_lower - model.market_price == 0)
    model.eq4 = Constraint(expr=demand - model.p_w1 - model.p_g1 - model.p_g2 == 0)
    model.comp1 = Complementarity(expr=complements(0 <= 20 - model.p_w1, model.mu_w1_upper >= 0))
    model.comp2 = Complementarity(expr=complements(0 <= model.p_w1, model.mu_w1_lower >= 0))
    model.comp3 = Complementarity(expr=complements(0 <= 50 - model.p_g1, model.mu_g1_upper >= 0))
    model.comp4 = Complementarity(expr=complements(0 <= model.p_g1, model.mu_g1_lower >= 0))
    model.comp5 = Complementarity(expr=complements(0 <= 100 - model.p_g2, model.mu_g2_upper >= 0))
    model.comp6 = Complementarity(expr=complements(0 <= model.p_g2, model.mu_g2_lower >= 0))

    # 4. solve the model
    solver = SolverFactory('pathampl')
    solver.solve(model)

    for var in vars:
        print(f"{var.name} = {round(var.value, 2)}")

def run_l2_mcp_elastic():
    # 0. input of the demand amount
    while True:
        try:
            max_demand = float(input("Enter the max demand amount: "))
            demand_price = float(input("Enter the demand price: "))
            break
        except:
            print("Please enter a non-negative number.")
            continue

    # 1. create a MCP model
    model = ConcreteModel()

    # 2. define variables
    model.p_w1 = Var()
    model.p_g1 = Var()
    model.p_g2 = Var()
    model.p_d1 = Var()
    model.mu_w1_lower = Var()
    model.mu_w1_upper = Var()
    model.mu_g1_lower = Var()
    model.mu_g1_upper = Var()
    model.mu_g2_lower = Var()
    model.mu_g2_upper = Var()
    model.mu_d1_lower = Var()
    model.mu_d1_upper = Var()
    model.market_price = Var()

    vars = [
        model.p_w1,
        model.p_g1,
        model.p_g2,
        model.p_d1,
        model.mu_w1_lower,
        model.mu_w1_upper,
        model.mu_g1_lower,
        model.mu_g1_upper,
        model.mu_g2_lower,
        model.mu_g2_upper,
        model.mu_d1_lower,
        model.mu_d1_upper,
        model.market_price,
    ]

    # 3. define equalities and complementarity conditions
    model.eq1 = Constraint(expr=0 + model.mu_w1_upper - model.mu_w1_lower - model.market_price == 0)
    model.eq2 = Constraint(expr=20 + model.mu_g1_upper - model.mu_g1_lower - model.market_price == 0)
    model.eq3 = Constraint(expr=30 + model.mu_g2_upper - model.mu_g2_lower - model.market_price == 0)
    model.eq4 = Constraint(expr=-demand_price + model.mu_d1_upper - model.mu_d1_lower + model.market_price == 0)
    model.eq5 = Constraint(expr=model.p_d1 - model.p_w1 - model.p_g1 - model.p_g2 == 0)
    model.comp1 = Complementarity(expr=complements(0 <= 20 - model.p_w1, model.mu_w1_upper >= 0))
    model.comp2 = Complementarity(expr=complements(0 <= model.p_w1, model.mu_w1_lower >= 0))
    model.comp3 = Complementarity(expr=complements(0 <= 50 - model.p_g1, model.mu_g1_upper >= 0))
    model.comp4 = Complementarity(expr=complements(0 <= model.p_g1, model.mu_g1_lower >= 0))
    model.comp5 = Complementarity(expr=complements(0 <= 100 - model.p_g2, model.mu_g2_upper >= 0))
    model.comp6 = Complementarity(expr=complements(0 <= model.p_g2, model.mu_g2_lower >= 0))
    model.comp7 = Complementarity(expr=complements(0 <= max_demand - model.p_d1, model.mu_d1_upper >= 0))
    model.comp8 = Complementarity(expr=complements(0 <= model.p_d1, model.mu_d1_lower >= 0))

    # 4. solve the model
    solver = SolverFactory('pathampl')
    solver.solve(model)

    for var in vars:
        print(f"{var.name} = {round(var.value)}")

def run_l3_mcp():
    # 0. input of the demand amount
    while True:
        try:
            max_demand = float(input("Enter the max demand amount: "))
            demand_price = float(input("Enter the demand price: "))
            line_capacity = float(input("Enter the line capacity: "))
            break
        except:
            print("Please enter a non-negative number.")
            continue

    # 1. create a MCP model
    model = ConcreteModel()

    # 2. define variables
    model.p_w1 = Var()
    model.p_g1 = Var()
    model.p_g2 = Var()
    model.p_d1 = Var()
    model.p_12 = Var()
    model.mu_w1_lower = Var()
    model.mu_w1_upper = Var()
    model.mu_g1_lower = Var()
    model.mu_g1_upper = Var()
    model.mu_g2_lower = Var()
    model.mu_g2_upper = Var()
    model.mu_d1_lower = Var()
    model.mu_d1_upper = Var()
    model.mu_12_lower = Var()
    model.mu_12_upper = Var()
    model.market_price_bus1 = Var()
    model.market_price_bus2 = Var()

    vars = [
        model.p_w1,
        model.p_g1,
        model.p_g2,
        model.p_d1,
        model.p_12,
        model.mu_w1_lower,
        model.mu_w1_upper,
        model.mu_g1_lower,
        model.mu_g1_upper,
        model.mu_g2_lower,
        model.mu_g2_upper,
        model.mu_d1_lower,
        model.mu_d1_upper,
        model.mu_12_lower,
        model.mu_12_upper,
        model.market_price_bus1,
        model.market_price_bus2,
    ]

    # 3. define equalities and complementarity conditions
    model.eq1 = Constraint(expr=0 + model.mu_w1_upper - model.mu_w1_lower - model.market_price_bus1 == 0)
    model.eq2 = Constraint(expr=20 + model.mu_g1_upper - model.mu_g1_lower - model.market_price_bus1 == 0)
    model.eq3 = Constraint(expr=30 + model.mu_g2_upper - model.mu_g2_lower - model.market_price_bus2 == 0)
    model.eq4 = Constraint(expr=-demand_price + model.mu_d1_upper - model.mu_d1_lower + model.market_price_bus2 == 0)
    model.eq5 = Constraint(expr=model.mu_12_upper - model.mu_12_lower + model.market_price_bus1 - model.market_price_bus2 == 0)
    model.eq6 = Constraint(expr=model.p_12 - model.p_w1 - model.p_g1 == 0)
    model.eq7 = Constraint(expr=model.p_d1 - model.p_12 - model.p_g2 == 0)
    model.comp1 = Complementarity(expr=complements(0 <= 20 - model.p_w1, model.mu_w1_upper >= 0))
    model.comp2 = Complementarity(expr=complements(0 <= model.p_w1, model.mu_w1_lower >= 0))
    model.comp3 = Complementarity(expr=complements(0 <= 50 - model.p_g1, model.mu_g1_upper >= 0))
    model.comp4 = Complementarity(expr=complements(0 <= model.p_g1, model.mu_g1_lower >= 0))
    model.comp5 = Complementarity(expr=complements(0 <= 100 - model.p_g2, model.mu_g2_upper >= 0))
    model.comp6 = Complementarity(expr=complements(0 <= model.p_g2, model.mu_g2_lower >= 0))
    model.comp7 = Complementarity(expr=complements(0 <= max_demand - model.p_d1, model.mu_d1_upper >= 0))
    model.comp8 = Complementarity(expr=complements(0 <= model.p_d1, model.mu_d1_lower >= 0))
    model.comp9 = Complementarity(expr=complements(0 <= line_capacity - model.p_12, model.mu_12_upper >= 0))
    model.comp10 = Complementarity(expr=complements(0 <= model.p_12 + line_capacity, model.mu_12_lower >= 0))
    
    # 4. solve the model
    solver = SolverFactory('pathampl')
    solver.solve(model)

    for var in vars:
        print(f"{var.name} = {round(var.value)}")

def run_l4_opt():
    import highspy

    # 1. Create a new model
    h = highspy.Highs()
    h.setOptionValue("output_flag", False) # mute the outputs

    # 2. Define decision variables
    p_d1 = h.addVariable()
    p_d2 = h.addVariable()
    p_g1 = h.addVariable()
    p_g2 = h.addVariable()

    # x0 = h.addVariable(lb = 0, ub = 4)
    # x1 = h.addVariable(lb = 1, ub = 7)

    # 3. Set the objective function
    social_welfare = (
            +40 * p_d1 +
            +35 * p_d2 +
            -12 * p_g1 + 
            -20 * p_g2
        )

    # 4. Add constraints
    h.addConstr(0 <= p_d1 <= 100)
    h.addConstr(0 <= p_d2 <= 50)  
    h.addConstr(0 <= p_g1 <= 100) 
    h.addConstr(0 <= p_g2 <= 100)
    h.addConstr(p_d1 + p_d2 - p_g1 - p_g2 == 0, "equality")

    # 5. Optimize the model
    h.maximize(social_welfare)
    h.run()

    # 6. Display the results
    if h.modelStatusToString(h.getModelStatus()) == "Optimal":
        print("\n--------------------------")
        print("---- Optimal Solution ----")
        print("--------------------------")

        solution = h.getSolution()
        info = h.getInfo()

        print("Optimal objective =", info.objective_function_value)
        print("Primal solution status =", h.solutionStatusToString(info.primal_solution_status))
        print("Dual solution status =", h.solutionStatusToString(info.dual_solution_status))
        print("Basis validity =", h.basisValidityToString(info.basis_validity))

        market_price = abs(solution.row_dual[-1])
        p_d1 = solution.col_value[0]
        p_d2 = solution.col_value[1]
        p_g1 = solution.col_value[2]
        p_g2 = solution.col_value[3]

        print(f"p_d1 = {round(p_d1, 2)}")
        print(f"p_d2 = {round(p_d2, 2)}")
        print(f"p_g1 = {round(p_g1, 2)}")
        print(f"p_g2 = {round(p_g2, 2)}")
        print(f"market_price = {round(market_price, 2)}")

def run_l4_mcp():
    # 1. create a MCP model
    model = ConcreteModel()

    # 2. define variables
    model.p_d1 = Var()
    model.p_d2 = Var()
    model.p_g1 = Var()
    model.p_g2 = Var()
    model.market_price = Var()
    model.mu_d1_lower = Var()
    model.mu_d1_upper = Var()
    model.mu_d2_lower = Var()
    model.mu_d2_upper = Var()
    model.mu_g1_lower = Var()
    model.mu_g1_upper = Var()
    model.mu_g2_lower = Var()
    model.mu_g2_upper = Var()

    vars = [
        model.p_d1,
        model.p_d2,
        model.p_g1,
        model.p_g2,
        model.market_price,
        model.mu_d1_lower,
        model.mu_d1_upper,
        model.mu_d2_lower,
        model.mu_d2_upper,
        model.mu_g1_lower,
        model.mu_g1_upper,
        model.mu_g2_lower,
        model.mu_g2_upper,
    ]

    # 3. define equalities and complementarity conditions
    model.eq1 = Constraint(expr=-40 + model.mu_d1_upper - model.mu_d1_lower + model.market_price == 0)
    model.eq2 = Constraint(expr=-35 + model.mu_d2_upper - model.mu_d2_lower + model.market_price == 0)
    model.eq3 = Constraint(expr=12 + model.mu_g1_upper - model.mu_g1_lower - model.market_price == 0)
    model.eq4 = Constraint(expr=20 + model.mu_g2_upper - model.mu_g2_lower - model.market_price == 0)
    model.eq5 = Constraint(expr=model.p_d1 + model.p_d2 - model.p_g1 - model.p_g2 == 0)
    model.comp1 = Complementarity(expr=complements(0 <= 100 - model.p_d1, model.mu_d1_upper >= 0))
    model.comp2 = Complementarity(expr=complements(0 <= model.p_d1, model.mu_d1_lower >= 0))
    model.comp3 = Complementarity(expr=complements(0 <= 50 - model.p_d2, model.mu_d2_upper >= 0))
    model.comp4 = Complementarity(expr=complements(0 <= model.p_d2, model.mu_d2_lower >= 0))
    model.comp5 = Complementarity(expr=complements(0 <= 100 - model.p_g1, model.mu_g1_upper >= 0))
    model.comp6 = Complementarity(expr=complements(0 <= model.p_g1, model.mu_g1_lower >= 0))
    model.comp7 = Complementarity(expr=complements(0 <= 80 - model.p_g2, model.mu_g2_upper >= 0))
    model.comp8 = Complementarity(expr=complements(0 <= model.p_g2, model.mu_g2_lower >= 0))

    # 4. solve the model
    solver = SolverFactory('pathampl')
    solver.solve(model)

    for var in vars:
        print(f"{var.name} = {round(var.value)}")

if __name__ == "__main__":
    run_l4_mcp()