# intro:
# 1. MAX and MIN assign different signs to dual due to the positive and negative coefficient in objective
# 2. Gurobi does not support strict inequality, so the bounds of variables are with "="
#    Gurobi does not support two-sided constraints, so should split the contraints
# 3. HiGHS by default without specifying the variable property, it is continuous
#    HiGHS supports two-sided constraints
# 4. Change the "demander_data" to different case to see the optimality

# 5. HiGHS is open-sourced solver, Gurobi is commerical with license, both with Python API
# 6. pulp, pyomo, ortools and so on are interfaces, not fundamental or straightforward

# data collected from Lecture 2
producer_data = {
    "w1": {
        "type": "wind",
        "unit": "MW",
        "pro_forecast": 20,
        "offer_price": 0,
    },

    "g1": {
        "type": "convention",
        "unit": "MW",
        "pro_forecast": 50,
        "offer_price": 20,
    },

    "g2": {
        "type": "convention",
        "unit": "MW",
        "pro_forecast": 100,
        "offer_price": 30,
    }
}

def UI() -> None:
    while True:
        try:
            max_amount = float(input("\nPlease enter the max demand amount (MW): "))
            print("If inelastic, set demand price large enough, e.g., 9999")
            price = float(input("Please enter the demand price ($/MW): "))
            break
        except ValueError:
            print("Invalid input. Please enter numeric values for amount and price.\n")
            continue 
 
    while True:
        model = input("Please enter the solver to use (gurobi/highs): ").lower()
        if model == "gurobi":
            gurobi_api(max_amount, price)
            break 
        elif model == "highs": 
            highs_api(max_amount, price)
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
    
def gurobi_api(max_amount, demand_price) -> None:
    import gurobipy as gp
    from gurobipy import GRB

    try:
        # 1. Create a new model
        m = gp.Model("Lecture_2_in_class_optimization_case")
        m.setParam('OutputFlag', 0)

        # 2. Define decision variables
        p_w1 = m.addVar(vtype=GRB.CONTINUOUS, name="wind_supply_amount")
        p_g1 = m.addVar(vtype=GRB.CONTINUOUS, name="g1_supply_amount")
        p_g2 = m.addVar(vtype=GRB.CONTINUOUS, name="g2_supply_amount")
        p_d1 = m.addVar(vtype=GRB.CONTINUOUS, name="demand_amount")

        # 3. Set the objective function
        social_welfare = (
                +demand_price * p_d1 +
                -producer_data["w1"]["offer_price"] * p_w1 + 
                -producer_data["g1"]["offer_price"] * p_g1 + 
                -producer_data["g2"]["offer_price"] * p_g2
            )

        m.setObjective(social_welfare, GRB.MAXIMIZE)

        # 4. Add constraints
        m.addConstr(p_w1 >= 0, "wind_lb") 
        m.addConstr(p_w1 <= producer_data["w1"]["pro_forecast"], "wind_up")
        m.addConstr(p_g1 >= 0, "g1_lb") 
        m.addConstr(p_g1 <= producer_data["g1"]["pro_forecast"], "g1_up") 
        m.addConstr(p_g2 >= 0, "g2_lb")
        m.addConstr(p_g2 <= producer_data["g2"]["pro_forecast"], "g2_up")
        m.addConstr(p_d1 - p_w1 - p_g1 - p_g2 == 0, "equality")
        m.addConstr(p_d1 >= 0, "demand_lb")
        m.addConstr(p_d1 <= max_amount, "demand_up")

        # 5. Optimize the model
        m.optimize()

        # 6. Display the results
        if m.status == GRB.OPTIMAL:
            print("\n--------------------------")
            print("---- Optimal Solution ----")
            print("--------------------------")
            print(f"Optimal social welfare: {m.ObjVal}")
            print(f"Optimal market (marginal) price: {abs(m.getConstrByName('equality').Pi)}")
            print(f"Optimal demand amount: {p_d1.X} MW")
            print(f"Demand price: {demand_price}")
            print(f"Optimal demand total utility: {p_d1.X * demand_price}\n")

            import pandas as pd
            from tabulate import tabulate

            market_price = abs(m.getConstrByName('equality').Pi)

            results = {
                "w1": {
                    "supply_MW": p_w1.X,
                    "offer_price": producer_data["w1"]["offer_price"],
                    "market_price": market_price,
                    "revenue": p_w1.X * market_price,
                    "cost": producer_data["w1"]["offer_price"] * p_w1.X,
                    "profit": p_w1.X * market_price - producer_data["w1"]["offer_price"] * p_w1.X,
                },
                "g1": {
                    "supply_MW": p_g1.X,
                    "offer_price": producer_data["g1"]["offer_price"],
                    "market_price": market_price,
                    "revenue": p_g1.X * market_price,
                    "cost": producer_data["g1"]["offer_price"] * p_g1.X,
                    "profit": p_g1.X * market_price - producer_data["g1"]["offer_price"] * p_g1.X,
                },
                "g2": {
                    "supply_MW": p_g2.X,
                    "offer_price": producer_data["g2"]["offer_price"],
                    "market_price": market_price,
                    "revenue": p_g2.X * market_price,
                    "cost": producer_data["g2"]["offer_price"] * p_g2.X,
                    "profit": p_g2.X * market_price - producer_data["g2"]["offer_price"] * p_g2.X,
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

def highs_api(max_amount, demand_price) -> None:
    import highspy

    # 1. Create a new model
    h = highspy.Highs()
    h.setOptionValue("output_flag", False) # mute the outputs

    # 2. Define decision variables
    p_w1 = h.addVariable()
    p_g1 = h.addVariable()
    p_g2 = h.addVariable()
    p_d1 = h.addVariable()

    # x0 = h.addVariable(lb = 0, ub = 4)
    # x1 = h.addVariable(lb = 1, ub = 7)

    # 3. Set the objective function
    social_welfare = (
            +demand_price * p_d1 +
            -producer_data["w1"]["offer_price"] * p_w1 + 
            -producer_data["g1"]["offer_price"] * p_g1 + 
            -producer_data["g2"]["offer_price"] * p_g2
        )

    # 4. Add constraints
    h.addConstr(0 <= p_w1 <= producer_data["w1"]["pro_forecast"], "wind_up")
    h.addConstr(0 <= p_g1 <= producer_data["g1"]["pro_forecast"], "g1_up")  
    h.addConstr(0 <= p_g2 <= producer_data["g2"]["pro_forecast"], "g2_up") 
    h.addConstr(0 <= p_d1 <= max_amount, "demand_range")
    h.addConstr(p_d1 - p_w1 - p_g1 - p_g2 == 0, "equality")

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
        p_w1 = solution.col_value[0]
        p_g1 = solution.col_value[1]
        p_g2 = solution.col_value[2]
        p_d1 = solution.col_value[3]

        print(f"Optimal social welfare: {info.objective_function_value}")
        print(f"Optimal market (marginal) price: {market_price}")
        print(f"Optimal demand amount: {p_d1} MW")
        print(f"Demand price: {demand_price}")
        print(f"Optimal demand total utility: {p_d1 * demand_price}\n")
        import pandas as pd
        from tabulate import tabulate

        results = {
            "w1": {
                "supply_MW": p_w1,
                "offer_price": producer_data["w1"]["offer_price"],
                "market_price": market_price,
                "revenue": p_w1 * market_price,
                "cost": producer_data["w1"]["offer_price"] * p_w1,
                "profit": (market_price - producer_data["w1"]["offer_price"]) * p_w1,
            },
            "g1": {
                "supply_MW": p_g1,
                "offer_price": producer_data["g1"]["offer_price"],
                "market_price": market_price,
                "revenue": p_g1 * market_price,
                "cost": producer_data["g1"]["offer_price"] * p_g1,
                "profit": (market_price - producer_data["g1"]["offer_price"]) * p_g1,
            },
            "g2": {
                "supply_MW": p_g2,
                "offer_price": producer_data["g2"]["offer_price"],
                "market_price": market_price,
                "revenue": p_g2 * market_price,
                "cost": producer_data["g2"]["offer_price"] * p_g2,
                "profit": (market_price - producer_data["g2"]["offer_price"]) * p_g2,
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
        print(f"The model is not optimal. Status: {h.modelStatusToString(h.getModelStatus())}")


if __name__ == "__main__":
    UI()