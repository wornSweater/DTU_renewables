def UI() -> None:
    while True:
        try:
            amount = float(input("\nPlease enter the regulation amount (positive is up/negative is down): "))
            break
        except ValueError:
            print("Invalid input. Please enter numeric values for amount and price.\n")
            continue 
 
    while True:
        model = input("Please enter the solver to use (gurobi/highs): ").lower()
        if model == "gurobi":
            gurobi_api(amount)
            break 
        elif model == "highs": 
            highs_api(amount)
            break 
        else: 
            print("\nInvalid solver selected. Try again.\n")
            continue

    while True:
        loop = input("\nWould like to run again? (y/n): ")
        if loop == "y":
            UI()
            break
        elif loop == "n":
            print("\nTerminating program.\n")
            return
        else:
            continue

def gurobi_api(regulation_amount):
    import gurobipy as gp
    from gurobipy import GRB

    # 1. Create a new model
    m = gp.Model("Lecture_5b_in_class_optimization_case")
    m.setParam('OutputFlag', 0) # mute the output details

    # 2. Define decision variables
    p_g2_up = m.addVar(lb=0, ub=80, vtype=GRB.CONTINUOUS, name="G2_up_regulation_amount")
    p_d1_up = m.addVar(lb=0, ub=30, vtype=GRB.CONTINUOUS, name="D1_up_regulation_amount")
    p_d1_curt = m.addVar(lb=0, ub=60, vtype=GRB.CONTINUOUS, name="D1_curtailment_amount")
    p_g2_dw = m.addVar(lb=0, ub=20, vtype=GRB.CONTINUOUS, name="G2_down_regulation_amount")

    # 3. Set the objective function
    regulation_cost = (
            +33 * p_g2_up +
            +40 * p_d1_up + 
            +500 * p_d1_curt + 
            -22 * p_g2_dw
        )

    m.setObjective(regulation_cost, GRB.MINIMIZE)

    # 4. Add supply-demand balance constraint for each node
    m.addConstr(p_g2_up + p_d1_up + p_d1_curt - p_g2_dw == regulation_amount, "balancing_market_equality")

    # 5. Optimize the model
    m.optimize()

    # 6. Display the results
    if m.status == GRB.OPTIMAL:
        print("\n--------------------------")
        print("---- Optimal Solution ----")
        print("--------------------------")
        print(f"Minimized balancing cost: {m.ObjVal}")
        print(f"Optimal balancing market (marginal) price: {abs(m.getConstrByName('balancing_market_equality').Pi)}")

        for v in m.getVars():
            print(f"{v.VarName}: {v.X}")
    elif m.status == GRB.INFEASIBLE:
        print("Optimization ended with status INFEASIBLE")
    elif m.status == GRB.UNBOUNDED:
        print("Optimization ended with status UNBOUNDED")
    else:   
        print(f"Optimization ended with status {m.status}")

def highs_api(regulation_amount):
    import highspy

    # 1. Create a new model
    h = highspy.Highs()
    h.setOptionValue("output_flag", False) # mute the outputs

    # 2. Define decision variables
    p_g2_up = h.addVariable(lb=0, ub=80)
    p_d1_up = h.addVariable(lb=0, ub=30)
    p_d1_curt = h.addVariable(lb=0, ub=60)
    p_g2_dw = h.addVariable(lb=0, ub=20)

    var_names = ["p_g2_up", "p_d1_up", "p_d1_curt", "p_g2_dw"]

    # 3. Set the objective function
    regulation_cost = (
            +33 * p_g2_up +
            +40 * p_d1_up + 
            +500 * p_d1_curt + 
            -22 * p_g2_dw
        )

    # 4. Add constraints
    h.addConstr(p_g2_up + p_d1_up + p_d1_curt - p_g2_dw == regulation_amount, "balancing_market_equality")

    # 5. Optimize the model
    h.minimize(regulation_cost)
    h.run()

    # 6. Display the results
    if h.modelStatusToString(h.getModelStatus()) == "Optimal":
        print("\n--------------------------")
        print("---- Optimal Solution ----")
        print("--------------------------")
        solution = h.getSolution()
        info = h.getInfo()
        print('Primal solution status = ', h.solutionStatusToString(info.primal_solution_status))
        print('Dual solution status = ', h.solutionStatusToString(info.dual_solution_status))
        print('Basis validity = ', h.basisValidityToString(info.basis_validity))
        print(f"Minimized balancing cost: {info.objective_function_value}")
        print(f"Optimal balancing market (marginal) price: {abs(solution.row_dual[0])}")
        for i, var in enumerate(var_names):
            print(f"{var}: {solution.col_value[i]}")
    else:
        print(f"Optimization ended with status {h.modelStatusToString(h.getModelStatus())}")

if __name__ == "__main__":
    UI()