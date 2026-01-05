# data collected from Lecture 3
producer_data = {
    "w1": {
        "type": "wind",
        "unit": "MW",
        "node": "bus_1",
        "pro_forecast": 20,
        "offer_price": 0,
    },

    "g1": {
        "type": "convention",
        "unit": "MW",
        "node": "bus_1",
        "pro_forecast": 50,
        "offer_price": 20,
    },

    "g2": {
        "type": "convention",
        "unit": "MW",
        "node": "bus_2",
        "pro_forecast": 100,
        "offer_price": 30,
    }
}

def UI() -> None:
    while True:
        try:
            amount = float(input("\nPlease enter the max demand amount (MW): "))
            price = float(input("Please enter the demand price ($/MW): "))
            line_capacity = float(input("Please enter the transmission line capacity (MW): "))
            break
        except ValueError:
            print("Invalid input. Please enter numeric values for amount and price.\n")
            continue 
 
    while True:
        model = input("Please enter the solver to use (gurobi/highs): ").lower()
        if model == "gurobi":
            gurobi_api(amount, price, line_capacity)
            break 
        elif model == "highs": 
            highs_api(amount, price, line_capacity)
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

def gurobi_api(max_amount, price, line_capacity) -> None:
    import gurobipy as gp
    from gurobipy import GRB

    try:
        # 1. Create a new model
        m = gp.Model("Lecture_3_in_class_optimization_case")
        m.setParam('OutputFlag', 0) # mute the output details

        # 2. Define decision variables
        p_w1 = m.addVar(lb=0, ub=producer_data["w1"]["pro_forecast"], vtype=GRB.CONTINUOUS, name="wind_supply_amount")
        p_g1 = m.addVar(lb=0, ub=producer_data["g1"]["pro_forecast"], vtype=GRB.CONTINUOUS, name="g1_supply_amount")
        p_g2 = m.addVar(lb=0, ub=producer_data["g2"]["pro_forecast"], vtype=GRB.CONTINUOUS, name="g2_supply_amount")
        p_d1 = m.addVar(lb=0, ub=max_amount, vtype=GRB.CONTINUOUS, name="demand_amount")
        p_line = m.addVar(lb=-line_capacity, ub=line_capacity, vtype=GRB.CONTINUOUS, name="transmission_amount")

        # 3. Set the objective function
        social_welfare = (
                +price * p_d1 +
                -producer_data["w1"]["offer_price"] * p_w1 + 
                -producer_data["g1"]["offer_price"] * p_g1 + 
                -producer_data["g2"]["offer_price"] * p_g2
            )

        m.setObjective(social_welfare, GRB.MAXIMIZE)

        # 4. Add supply-demand balance constraint for each node
        m.addConstr(p_w1 + p_g1 - p_line == 0, "bus_1_equality") # bus 1 balance
        m.addConstr(p_d1 - p_g2 - p_line == 0, "bus_2_equality") # bus 2 balance

        # 5. Optimize the model
        m.optimize()

        # 6. Display the results
        if m.status == GRB.OPTIMAL:
            print("\n--------------------------")
            print("---- Optimal Solution ----")
            print("--------------------------")
            print(f"Optimal social welfare: {m.ObjVal}")
            print(f"Optimal bus1 market (marginal) price: {abs(m.getConstrByName('bus_1_equality').Pi)}")
            print(f"Optimal bus2 market (marginal) price: {abs(m.getConstrByName('bus_2_equality').Pi)}")

            bus_1_market_price = abs(m.getConstrByName('bus_1_equality').Pi)
            bus_2_market_price = abs(m.getConstrByName('bus_2_equality').Pi)
            print(f"Demand location: bus_2, price: {bus_2_market_price}")
            print(f"Optimal demand amount: {p_d1.X} MW")
            print(f"Demand price: {price}")
            print(f"Demand total utility: {p_d1.X * price}\n")
            print(f"w1 suppply amount (p_w1: MW): {p_w1.X}")
            print(f"g1 suppply amount (p_g1: MW): {p_g1.X}")
            print(f"g2 suppply amount (p_g2: MW): {p_g2.X}")
            print(f"d1 demand amount (p_d1: MW): {p_d1.X}")
            print(f"Transmission line capacity used (p_line: MW): {p_line.X}")

            print(f"Demand total payment is: {p_d1.X * abs(m.getConstrByName('bus_2_equality').Pi)}")
            print(f"Supply total revenue is: {(p_w1.X + p_g1.X) * bus_1_market_price + p_g2.X * bus_2_market_price}")
            print(f"Congestion rent is: {abs(bus_1_market_price - bus_2_market_price) * abs(p_line.X)}, unit price is {abs(bus_1_market_price - bus_2_market_price)}\n")

            import pandas as pd
            from tabulate import tabulate

            results = {
                "w1": {
                    "node": producer_data["w1"]["node"],
                    "supply_MW": p_w1.X,
                    "offer_price": producer_data["w1"]["offer_price"],
                    "market_price": bus_1_market_price,
                    "revenue": p_w1.X * bus_1_market_price,
                    "cost": producer_data["w1"]["offer_price"] * p_w1.X,
                    "profit": p_w1.X * bus_1_market_price - producer_data["w1"]["offer_price"] * p_w1.X,
                },
                "g1": {
                    "node": producer_data["g1"]["node"],
                    "supply_MW": p_g1.X,
                    "offer_price": producer_data["g1"]["offer_price"],
                    "market_price": bus_1_market_price,
                    "revenue": p_g1.X * bus_1_market_price,
                    "cost": producer_data["g1"]["offer_price"] * p_g1.X,
                    "profit": p_g1.X * bus_1_market_price - producer_data["g1"]["offer_price"] * p_g1.X,
                },
                "g2": {
                    "node": producer_data["g2"]["node"],
                    "supply_MW": p_g2.X,
                    "offer_price": producer_data["g2"]["offer_price"],
                    "market_price": bus_2_market_price,
                    "revenue": p_g2.X * bus_2_market_price,
                    "cost": producer_data["g2"]["offer_price"] * p_g2.X,
                    "profit": p_g2.X * bus_2_market_price - producer_data["g2"]["offer_price"] * p_g2.X,
                },
            }
            df = pd.DataFrame.from_dict(results, orient="index")

            print(
                tabulate(
                    df.reset_index(names="producer"),
                    headers="keys",
                    tablefmt="psql",
                    floatfmt=".2f",
                    showindex=False,
                )
            )

        elif m.status == GRB.INF_OR_UNBD:
            print("Model is infeasible or unbounded.")
        else:
            print(f"Optimization ended with status {m.status}")

    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")

    except AttributeError:
        print("Encountered an attribute error.")

def highs_api(max_amount, price, line_capacity) -> None:
    import highspy

    # 1. Create a new model
    h = highspy.Highs()
    h.setOptionValue("output_flag", False) # mute the outputs

    # 2. Define decision variables
    # by default without specifying the variable property, it is continuous
    p_w1 = h.addVariable(lb=0, ub=producer_data["w1"]["pro_forecast"])
    p_g1 = h.addVariable(lb=0, ub=producer_data["g1"]["pro_forecast"])
    p_g2 = h.addVariable(lb=0, ub=producer_data["g2"]["pro_forecast"])
    p_d1 = h.addVariable(lb=0, ub=max_amount)
    p_line = h.addVariable(lb=-line_capacity, ub=line_capacity)

    var_names = ["p_w1", "p_g1", "p_g2", "p_d1", "p_line"]

    # 3. Set the objective function
    social_welfare = (
            +price * p_d1 +
            -producer_data["w1"]["offer_price"] * p_w1 + 
            -producer_data["g1"]["offer_price"] * p_g1 + 
            -producer_data["g2"]["offer_price"] * p_g2
        )

    # 4. Add constraints
    h.addConstr(p_w1 + p_g1 - p_line == 0, "bus_1_equality") # bus 1 demand node supply-demand balance
    h.addConstr(p_d1 - p_g2 - p_line == 0, "bus_2_equality") # bus 2 supply-demand balance

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
        print('Primal solution status = ', h.solutionStatusToString(info.primal_solution_status))
        print('Dual solution status = ', h.solutionStatusToString(info.dual_solution_status))
        print('Basis validity = ', h.basisValidityToString(info.basis_validity))

        bus_1_market_price = abs(solution.row_dual[0])
        bus_2_market_price = abs(solution.row_dual[1])
        p_w1 = solution.col_value[0]
        p_g1 = solution.col_value[1]
        p_g2 = solution.col_value[2]
        p_d1 = solution.col_value[3]
        p_line = solution.col_value[4]
        print(f"Optimal social welfare: {info.objective_function_value}")
        print(f"Optimal bus1 market (marginal) price: {bus_1_market_price}")
        print(f"Optimal bus2 market (marginal) price: {bus_2_market_price}")
        print(f"Demand location: bus_2, price: {bus_2_market_price}")
        print(f"Optimal demand amount: {p_d1} MW")
        print(f"Demand price: {price}")
        print(f"Demand total utility: {p_d1 * price}\n")

        print(f"w1 suppply amount (p_w1: MW): {p_w1}")
        print(f"g1 suppply amount (p_g1: MW): {p_g1}")
        print(f"g2 suppply amount (p_g2: MW): {p_g2}")
        print(f"d1 demand amount (p_d1: MW): {p_d1}")
        print(f"Transmission line capacity used (p_line: MW): {p_line}")
        print(f"Demand total payment is: {p_d1 * bus_2_market_price}")
        print(f"Supply total revenue is: {(p_w1 + p_g1) * bus_1_market_price + p_g2 * bus_2_market_price}")
        print(f"Congestion rent is: {abs(bus_1_market_price - bus_2_market_price) * abs(p_line)}, unit price is {abs(bus_1_market_price - bus_2_market_price)}\n")

        import pandas as pd
        from tabulate import tabulate

        results = {
            "w1": {
                "node": producer_data["w1"]["node"],
                "supply_MW": p_w1,
                "offer_price": producer_data["w1"]["offer_price"],
                "market_price": bus_1_market_price,
                "revenue": p_w1 * bus_1_market_price,
                "cost": producer_data["w1"]["offer_price"] * p_w1,
                "profit": p_w1 * bus_1_market_price - producer_data["w1"]["offer_price"] * p_w1,
            },
            "g1": {
                "node": producer_data["g1"]["node"],
                "supply_MW": p_g1,
                "offer_price": producer_data["g1"]["offer_price"],
                "market_price": bus_1_market_price,
                "revenue": p_g1 * bus_1_market_price,
                "cost": producer_data["g1"]["offer_price"] * p_g1,
                "profit": p_g1 * bus_1_market_price - producer_data["g1"]["offer_price"] * p_g1,
            },
            "g2": {
                "node": producer_data["g2"]["node"],
                "supply_MW": p_g2,
                "offer_price": producer_data["g2"]["offer_price"],
                "market_price": bus_2_market_price,
                "revenue": p_g2 * bus_2_market_price,
                "cost": producer_data["g2"]["offer_price"] * p_g2,
                "profit": p_g2 * bus_2_market_price - producer_data["g2"]["offer_price"] * p_g2,
            },
        }
        df = pd.DataFrame.from_dict(results, orient="index")

        print(
            tabulate(
                df.reset_index(names="producer"),
                headers="keys",
                tablefmt="psql",
                floatfmt=".2f",
                showindex=False,
            )
        )
    else:
        print(f"Optimization ended with status {h.modelStatusToString(h.getModelStatus())}")
        

if __name__ == "__main__":
    UI()