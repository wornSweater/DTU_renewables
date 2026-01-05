# 1. Place 'using' statements at the top level of your script
using JuMP
using HiGHS
using Gurobi

# 2. Initialize the model and specify the HiGHS optimizer
# 2.1 Gurobi is possible here if with license
model = Model(HiGHS.Optimizer)

# Optional: silence the solver output if needed
set_silent(model) 

# 3.1 Read all the parameters
print("Please enter the max demand (MWh): ")
max_demand = parse(Float64, readline())
print("If inelastic demand, please enter a large price eg. 9999")
print("Please enter the demand price: ")
demand_price = parse(Float64, readline())
print("Please enter the line capacity: ")
line_capacity = parse(Float64, readline())

# 3. Define the variables with their bounds
@variables(model, begin
    0 <= p_w1 <= 20
    0 <= p_g1 <= 50
    0 <= p_g2 <= 100
    0 <= p_d1 <= max_demand
    -line_capacity <= p_line <= line_capacity
end)

# 4. Define the objective function (Minimize in this case)
social_welfare = demand_price * p_d1 - 0 * p_w1 - 20 * p_g1 - 30 * p_g2
@objective(model, Max, social_welfare)

# 5. Define the constraints
@constraints(model, begin
    balance_node_1, p_line - p_w1 - p_g1 == 0
    balance_node_2, p_d1 - p_g2 - p_line == 0
end)

# 6. Solve the optimization problem
optimize!(model)

# 7. Check the solution status and print results
if termination_status(model) == MOI.OPTIMAL
    println("Optimization Successful!")
    println("Objective value: ", objective_value(model))
    println("Optimal p_w1: ", value(p_w1))
    println("Optimal p_g1: ", value(p_g1))
    println("Optimal p_g2: ", value(p_g2))
    println("Optimal p_d1: ", value(p_d1))
    println("Optimal p_line: ", value(p_line))
    println("Market price of node 1 is: ", abs(dual(balance_node_1)))
    println("Market price of node 2 is: ", abs(dual(balance_node_2)))
    println("Congestion rent is: ", abs(dual(balance_node_1) - dual(balance_node_2)) * value(p_line))
else
    println("Optimization terminated with status: ", termination_status(model))
end