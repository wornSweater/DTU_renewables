def UI() -> None:
    while True:
        model = input("Please enter the solver to use (gurobi/highs): ").lower()
        if model == "gurobi":
            gurobi_api()
            break 
        elif model == "highs": 
            highs_api()
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

def gurobi_api():
    import gurobipy as gp
    from gurobipy import GRB

    # 1. Create a new model
    m = gp.Model("Lecture_6_in_class_optimization_case_capacity_market")
    m.setParam('OutputFlag', 0) # mute the output details

    # 2. Define decision variables
    r_g1_dw = m.addVar(lb=0, ub=5, vtype=GRB.CONTINUOUS, name="G1_dw_reserve")
    r_g1_up = m.addVar(lb=0, ub=5, vtype=GRB.CONTINUOUS, name="G1_up_reserve")
    r_g2_dw = m.addVar(lb=0, ub=50, vtype=GRB.CONTINUOUS, name="G2_dw_reserve")
    r_g2_up = m.addVar(lb=0, ub=50, vtype=GRB.CONTINUOUS, name="G2_up_reserve")

    r_g1_dw_opt, r_g1_up_opt, r_g2_dw_opt, r_g2_up_opt = 0, 0, 0, 0

    # 3. Set the objective function
    reserve_cost = (
            +1 * r_g1_dw +
            +1 * r_g1_up + 
            +2 * r_g2_dw + 
            +2 * r_g2_up
        )

    m.setObjective(reserve_cost, GRB.MINIMIZE)

    # 4. Add supply-demand balance constraint for each node
    m.addConstr(r_g1_dw + r_g2_dw == 35, "down_reserve_balance")
    m.addConstr(r_g1_up + r_g2_up == 40, "up_reserve_balance")

    # 5. Optimize the model
    m.optimize()

    # 6. Display the results
    if m.status == GRB.OPTIMAL:
        r_g1_dw_opt, r_g1_up_opt, r_g2_dw_opt, r_g2_up_opt = r_g1_dw.X, r_g1_up.X, r_g2_dw.X, r_g2_up.X
        print("\n-----------------------------------------")
        print("---- Reserve Market Optimal Solution ----")
        print("-----------------------------------------")
        print(f"Minimized reserve cost: {m.ObjVal}")
        print(f"Optimal down reserve price: {abs(m.getConstrByName('down_reserve_balance').Pi)}")
        print(f"Optimal up reserve price: {abs(m.getConstrByName('up_reserve_balance').Pi)}")

        for v in m.getVars():
            print(f"{v.VarName}: {v.X}")

    elif m.status == GRB.INFEASIBLE:
        print("Optimization ended with status INFEASIBLE")
    elif m.status == GRB.UNBOUNDED:
        print("Optimization ended with status UNBOUNDED")
    else:   
        print(f"Optimization ended with status {m.status}")

    # 1. Create a new model
    m = gp.Model("Lecture_6_in_class_optimization_case_dayahead_market")
    m.setParam('OutputFlag', 0) # mute the output details

    # 2. Define decision variables
    p_w1 = m.addVar(lb=0, ub=20, vtype=GRB.CONTINUOUS, name="W1_supply")
    p_g1 = m.addVar(lb=r_g1_dw_opt, ub=50-r_g1_up_opt, vtype=GRB.CONTINUOUS, name="G1_supply")
    p_g2 = m.addVar(lb=r_g2_dw_opt, ub=100-r_g2_up_opt, vtype=GRB.CONTINUOUS, name="G2_supply")
    p_d1 = m.addVar(lb=0, ub=90, vtype=GRB.CONTINUOUS, name="D1_demand")

    # 3. Set the objective function
    social_welfare = (
            +40 * p_d1 +
            - 0 * p_w1 + 
            -20 * p_g1 + 
            -30 * p_g2
        )

    m.setObjective(social_welfare, GRB.MAXIMIZE)

    # 4. Add supply-demand balance constraint for each node
    m.addConstr(p_d1 - p_w1 - p_g1 - p_g2 == 0, "supply_demand_balance")

    # 5. Optimize the model
    m.optimize()

    # 6. Display the results
    if m.status == GRB.OPTIMAL:
        print("\n-------------------------------------------")
        print("---- Day-ahead Market Optimal Solution ----")
        print("-------------------------------------------")
        print(f"Maximized social welfare: {m.ObjVal}")
        print(f"Optimal day-ahead market clearing price: {abs(m.getConstrByName('supply_demand_balance').Pi)}")

        for v in m.getVars():
            print(f"{v.VarName}: {v.X}")

    elif m.status == GRB.INFEASIBLE:
        print("Optimization ended with status INFEASIBLE")
    elif m.status == GRB.UNBOUNDED:
        print("Optimization ended with status UNBOUNDED")
    else:   
        print(f"Optimization ended with status {m.status}")

    # 1. Create a new model
    m = gp.Model("Lecture_6_in_class_optimization_case_balancing_market")
    m.setParam('OutputFlag', 0) # mute the output details

    # 2. Define decision variables
    p_g1_up = m.addVar(lb=0, ub=r_g1_up_opt, vtype=GRB.CONTINUOUS, name="G1_up_regulation")
    p_g2_up = m.addVar(lb=0, ub=r_g2_up_opt, vtype=GRB.CONTINUOUS, name="G2_up_regulation")
    p_d1_curt = m.addVar(lb=0, ub=90, vtype=GRB.CONTINUOUS, name="D1_curt_regulation")
    p_g1_dw = m.addVar(lb=0, ub=r_g1_dw_opt, vtype=GRB.CONTINUOUS, name="G1_dw_regulation")
    p_g2_dw = m.addVar(lb=0, ub=r_g2_dw_opt, vtype=GRB.CONTINUOUS, name="G2_dw_regulation")

    # 3. Set the objective function
    balancing_cost = (
            +22  * p_g1_up +
            +33  * p_g2_up + 
            +500 * p_d1_curt + 
            -17  * p_g1_dw +
            -27  * p_g2_dw
        )

    m.setObjective(balancing_cost, GRB.MINIMIZE)

    # 4. Add supply-demand balance constraint for each node
    m.addConstr(p_g1_up + p_g2_up + p_d1_curt - p_g1_dw - p_g2_dw == 15, "balancing_balance")

    # 5. Optimize the model
    m.optimize()

    # 6. Display the results
    if m.status == GRB.OPTIMAL:
        print("\n-------------------------------------------")
        print("---- Balancing Market Optimal Solution ----")
        print("-------------------------------------------")
        print(f"Minimized balancing cost: {m.ObjVal}")
        print(f"Optimal balancing market clearing price: {abs(m.getConstrByName('balancing_balance').Pi)}")

        for v in m.getVars():
            print(f"{v.VarName}: {v.X}")

    elif m.status == GRB.INFEASIBLE:
        print("Optimization ended with status INFEASIBLE")
    elif m.status == GRB.UNBOUNDED:
        print("Optimization ended with status UNBOUNDED")
    else:   
        print(f"Optimization ended with status {m.status}")

def highs_api():
    import highspy as hp
    
    # =============================================
    # 1. RESERVE MARKET OPTIMIZATION
    # =============================================
    print("\n-----------------------------------------")
    print("---- Reserve Market Optimal Solution ----")
    print("-----------------------------------------")
    
    h = hp.Highs()
    h.setOptionValue("log_to_console", False)
    
    # Variables: r_g1_dw, r_g1_up, r_g2_dw, r_g2_up
    h.addVar(0, 5)    # r_g1_dw (index 0)
    h.addVar(0, 5)    # r_g1_up (index 1)
    h.addVar(0, 50)   # r_g2_dw (index 2)
    h.addVar(0, 50)   # r_g2_up (index 3)
    
    # Objective: minimize 1*r_g1_dw + 1*r_g1_up + 2*r_g2_dw + 2*r_g2_up
    h.changeColsCost(4, [0, 1, 2, 3], [1.0, 1.0, 2.0, 2.0])
    h.changeColsIntegrality(4, [0, 1, 2, 3], [hp.HighsVarType.kContinuous]*4)
    
    # Constraints
    # r_g1_dw + r_g2_dw == 35
    h.addRow(35, 35, 2, [0, 2], [1.0, 1.0])
    
    # r_g1_up + r_g2_up == 40
    h.addRow(40, 40, 2, [1, 3], [1.0, 1.0])
    
    # Set to minimization
    h.changeObjectiveSense(hp.ObjSense.kMinimize)
    
    # Solve
    h.run()
    
    # Get solution
    solution = h.getSolution()
    info = h.getInfo()
    
    r_g1_dw_opt = solution.col_value[0]
    r_g1_up_opt = solution.col_value[1]
    r_g2_dw_opt = solution.col_value[2]
    r_g2_up_opt = solution.col_value[3]
    
    print(f"Minimized reserve cost: {info.objective_function_value}")
    print(f"Optimal down reserve price: {abs(solution.row_dual[0])}")
    print(f"Optimal up reserve price: {abs(solution.row_dual[1])}")
    print(f"G1_dw_reserve: {r_g1_dw_opt}")
    print(f"G1_up_reserve: {r_g1_up_opt}")
    print(f"G2_dw_reserve: {r_g2_dw_opt}")
    print(f"G2_up_reserve: {r_g2_up_opt}")
    
    # =============================================
    # 2. DAY-AHEAD MARKET OPTIMIZATION
    # =============================================
    print("\n-------------------------------------------")
    print("---- Day-ahead Market Optimal Solution ----")
    print("-------------------------------------------")
    
    h2 = hp.Highs()
    h2.setOptionValue("log_to_console", False)
    
    # Variables: p_w1, p_g1, p_g2, p_d1
    h2.addVar(0, 20)                          # p_w1 (index 0)
    h2.addVar(r_g1_dw_opt, 50-r_g1_up_opt)   # p_g1 (index 1)
    h2.addVar(r_g2_dw_opt, 100-r_g2_up_opt)  # p_g2 (index 2)
    h2.addVar(0, 90)                          # p_d1 (index 3)
    
    # Objective: maximize 40*p_d1 - 0*p_w1 - 20*p_g1 - 30*p_g2
    # For maximization, negate coefficients and minimize
    h2.changeColsCost(4, [0, 1, 2, 3], [0.0, 20.0, 30.0, -40.0])
    h2.changeColsIntegrality(4, [0, 1, 2, 3], [hp.HighsVarType.kContinuous]*4)
    
    # Constraint: p_d1 - p_w1 - p_g1 - p_g2 == 0
    # Rearranged: -p_w1 - p_g1 - p_g2 + p_d1 == 0
    h2.addRow(0, 0, 4, [0, 1, 2, 3], [-1.0, -1.0, -1.0, 1.0])
    
    # Set to minimization (we negated objective for maximization)
    h2.changeObjectiveSense(hp.ObjSense.kMinimize)
    
    # Solve
    h2.run()
    
    # Get solution
    solution2 = h2.getSolution()
    info2 = h2.getInfo()
    
    print(f"Maximized social welfare: {-info2.objective_function_value}")
    print(f"Optimal day-ahead market clearing price: {abs(solution2.row_dual[0])}")
    print(f"W1_supply: {solution2.col_value[0]}")
    print(f"G1_supply: {solution2.col_value[1]}")
    print(f"G2_supply: {solution2.col_value[2]}")
    print(f"D1_demand: {solution2.col_value[3]}")
    
    # =============================================
    # 3. BALANCING MARKET OPTIMIZATION
    # =============================================
    print("\n-------------------------------------------")
    print("---- Balancing Market Optimal Solution ----")
    print("-------------------------------------------")
    
    h3 = hp.Highs()
    h3.setOptionValue("log_to_console", False)
    
    # Variables: p_g1_up, p_g2_up, p_d1_curt, p_g1_dw, p_g2_dw
    h3.addVar(0, r_g1_up_opt)  # p_g1_up (index 0)
    h3.addVar(0, r_g2_up_opt)  # p_g2_up (index 1)
    h3.addVar(0, 90)           # p_d1_curt (index 2)
    h3.addVar(0, r_g1_dw_opt)  # p_g1_dw (index 3)
    h3.addVar(0, r_g2_dw_opt)  # p_g2_dw (index 4)
    
    # Objective: minimize 22*p_g1_up + 33*p_g2_up + 500*p_d1_curt - 17*p_g1_dw - 27*p_g2_dw
    h3.changeColsCost(5, [0, 1, 2, 3, 4], [22.0, 33.0, 500.0, -17.0, -27.0])
    h3.changeColsIntegrality(5, [0, 1, 2, 3, 4], [hp.HighsVarType.kContinuous]*5)
    
    # Constraint: p_g1_up + p_g2_up + p_d1_curt - p_g1_dw - p_g2_dw == 15
    h3.addRow(15, 15, 5, [0, 1, 2, 3, 4], [1.0, 1.0, 1.0, -1.0, -1.0])
    
    # Set to minimization
    h3.changeObjectiveSense(hp.ObjSense.kMinimize)
    
    # Solve
    h3.run()
    
    # Get solution
    solution3 = h3.getSolution()
    info3 = h3.getInfo()
    
    print(f"Minimized balancing cost: {info3.objective_function_value}")
    print(f"Optimal balancing market clearing price: {abs(solution3.row_dual[0])}")
    print(f"G1_up_regulation: {solution3.col_value[0]}")
    print(f"G2_up_regulation: {solution3.col_value[1]}")
    print(f"D1_curt_regulation: {solution3.col_value[2]}")
    print(f"G1_dw_regulation: {solution3.col_value[3]}")
    print(f"G2_dw_regulation: {solution3.col_value[4]}")

# Run the optimization
if __name__ == "__main__":
    UI()