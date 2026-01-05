using JuMP
using HiGHS
using Gurobi

# =========================================================
# =============== 1. RESERVE MARKET =======================
# =========================================================
model = Model(HiGHS.Optimizer)
set_silent(model)

@variable(model, 0 <= r_g1_dw <= 5)
@variable(model, 0 <= r_g1_up <= 5)
@variable(model, 0 <= r_g2_dw <= 50)
@variable(model, 0 <= r_g2_up <= 50)

@objective(model, Min,
    1 * r_g1_dw +
    1 * r_g1_up +
    2 * r_g2_dw +
    2 * r_g2_up
)

c_dw = @constraint(model, r_g1_dw + r_g2_dw == 35)
c_up = @constraint(model, r_g1_up + r_g2_up == 40)

optimize!(model)

r_g1_dw_opt = value(r_g1_dw)
r_g1_up_opt = value(r_g1_up)
r_g2_dw_opt = value(r_g2_dw)
r_g2_up_opt = value(r_g2_up)

println("\n-----------------------------------------")
println("---- Reserve Market Optimal Solution ----")
println("-----------------------------------------")
println("Minimized reserve cost: ", objective_value(model))
println("Optimal down reserve price: ", abs(dual(c_dw)))
println("Optimal up reserve price: ", abs(dual(c_up)))

println("G1_dw_reserve: ", r_g1_dw_opt)
println("G1_up_reserve: ", r_g1_up_opt)
println("G2_dw_reserve: ", r_g2_dw_opt)
println("G2_up_reserve: ", r_g2_up_opt)

# =========================================================
# =============== 2. DAY-AHEAD MARKET =====================
# =========================================================
model = Model(HiGHS.Optimizer)
set_silent(model)

@variable(model, 0 <= p_w1 <= 20)
@variable(model, r_g1_dw_opt <= p_g1 <= 50 - r_g1_up_opt)
@variable(model, r_g2_dw_opt <= p_g2 <= 100 - r_g2_up_opt)
@variable(model, 0 <= p_d1 <= 90)

@objective(model, Max,
    40 * p_d1 -
    20 * p_g1 -
    30 * p_g2
)

c_da = @constraint(model, p_d1 - p_w1 - p_g1 - p_g2 == 0)

optimize!(model)

println("\n-------------------------------------------")
println("---- Day-ahead Market Optimal Solution ----")
println("-------------------------------------------")
println("Maximized social welfare: ", objective_value(model))
println("Optimal day-ahead market clearing price: ", abs(dual(c_da)))

println("W1_supply: ", value(p_w1))
println("G1_supply: ", value(p_g1))
println("G2_supply: ", value(p_g2))
println("D1_demand: ", value(p_d1))

# =========================================================
# =============== 3. BALANCING MARKET =====================
# =========================================================
model = Model(HiGHS.Optimizer)
set_silent(model)

@variable(model, 0 <= p_g1_up <= r_g1_up_opt)
@variable(model, 0 <= p_g2_up <= r_g2_up_opt)
@variable(model, 0 <= p_d1_curt <= 90)
@variable(model, 0 <= p_g1_dw <= r_g1_dw_opt)
@variable(model, 0 <= p_g2_dw <= r_g2_dw_opt)

@objective(model, Min,
    22  * p_g1_up +
    33  * p_g2_up +
    500 * p_d1_curt -
    17  * p_g1_dw -
    27  * p_g2_dw
)

c_bal = @constraint(
    model,
    p_g1_up + p_g2_up + p_d1_curt -
    p_g1_dw - p_g2_dw == 15
)

optimize!(model)

println("\n-------------------------------------------")
println("---- Balancing Market Optimal Solution ----")
println("-------------------------------------------")
println("Minimized balancing cost: ", objective_value(model))
println("Optimal balancing market clearing price: ", abs(dual(c_bal)))

println("G1_up_regulation: ", value(p_g1_up))
println("G2_up_regulation: ", value(p_g2_up))
println("D1_curt_regulation: ", value(p_d1_curt))
println("G1_dw_regulation: ", value(p_g1_dw))
println("G2_dw_regulation: ", value(p_g2_dw))
