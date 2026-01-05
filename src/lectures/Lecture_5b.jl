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
print("Please enter the regulation demand (MWh): ")
regulation_amount = parse(Float64, readline())

# 3.2 Define the variables with their bounds
@variables(model, begin
    0 <= p_g2_up <= 80
    0 <= p_d1_up <= 30
    0 <= p_d1_curt <= 60
    0 <= p_g2_dw <= 20
end)


# 4. Define the objective function (Minimize in this case)
regulation_cost = 33 * p_g2_up + 40 * p_d1_up + 500 * p_d1_curt - 22 * p_g2_dw
@objective(model, Min, regulation_cost)

# 5. Define the constraints
@constraint(model, balance, p_g2_up + p_d1_up + p_d1_curt - p_g2_dw == regulation_amount)

# 6. Solve the optimization problem
optimize!(model)

# 7. Check the solution status and print results
if termination_status(model) == MOI.OPTIMAL
    println("Optimization Successful!")
    println("Objective value: ", objective_value(model))
    println("Optimal p_g2_up: ", value(p_g2_up))
    println("Optimal p_d1_up: ", value(p_d1_up))
    println("Optimal p_d1_curt: ", value(p_d1_curt))
    println("Optimal p_g2_dw: ", value(p_g2_dw))
    println("Market price is: ", abs(dual(balance)))
else
    println("Optimization terminated with status: ", termination_status(model))
end