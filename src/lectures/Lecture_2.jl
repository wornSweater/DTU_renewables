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
println("If inelastic demand, enter a very high value, eg. 9999")
print("Please enter the demand price: ")
demand_price = parse(Float64, readline())

# 3.2 Define the variables with their bounds
@variables(model, begin
    0 <= p_w1 <= 20
    0 <= p_g1 <= 50
    0 <= p_g2 <= 100
    0 <= p_d1 <= max_demand
end)

# 4. Define the objective function (Minimize in this case)
social_welfare = demand_price * p_d1 - 0 * p_w1 - 20 * p_g1 - 30 * p_g2
@objective(model, Max, social_welfare)

# 5. Define the constraints
@constraint(model, balance, p_d1 - p_w1 - p_g1 - p_g2 == 0)

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
    println("Market price is: ", abs(dual(balance)))
else
    println("Optimization terminated with status: ", termination_status(model))
end