# ⚡ Renewables in Electricity Markets - Content
* [Project Overview](#-project-overview)
* [Motivation & Vision](#-motivation--vision)
* [Tech Stack](#-tech-stack)
    * [Introduction](#introduction)
    * [Python](#python)
    * [Julia](#julia)
    * [PATH Solver](#path-solver)
* [Project Structure](#-project-strucutre)
* [Case Study and Coding](#-case-study-and-coding)
    * [Python Dependencies and Script Running](#python-dependencies-and-script-running)
    * [Julia Dependencies and Script Running](#julia-dependencies-and-script-running)

# 📖 Project Overview

This project provides the code implementation for cases discussed by **[Prof. Jalal Kazempour](https://www.jalalkazempour.com/home)** for the **[DTU](https://www.dtu.dk/english/)** (Technical University of Denmark) Master’s course **[Renewables in Electricity Markets](https://www.jalalkazempour.com/teaching/msc-renewables-in-electricity-markets)**. The goal of this repository is to bridge the gap between theoretical lecture material and practical numerical modeling. It is designed to support students who may be new to optimization modeling / coding tools like Gurobi or HiGHS.

Please click the links below to find more information:

📘 [Course description](https://kurser.dtu.dk/course/46755)

🎥 [Lecture recordings](https://www.jalalkazempour.com/teaching/msc-renewables-in-electricity-markets)

▶️ [YouTube playlist](https://www.youtube.com/playlist?list=PLe7H9pun_r8bsWrLZ483DhVt8zvU4jv8P)

# 💡 Motivation & Vision

This project exists primarily out of the **author’s interest with European electricity markets after finishing a Belgian electricity balancing market project, getting some energy utilities' interveiws and watching all online lectures of this course**. Coming from an interdisciplinary academic background - Language Study, Translation, Econometrics, Operations Research, Artificial Intelligence, and Quantitative Finance, the author previously felt uncertain about long-term career direction. This course played a pivotal role in clarifying that uncertainty. It revealed electricity markets perfectly integrate all of these disciplines, and these elements form a coherent and intellectually rich field that bridges theory and real-world applications. (More about the Author: 😎 [LinkedIn](https://www.linkedin.com/in/xiaojing-lu-19b371227/) |
😉 [GitHub](https://github.com/wornSweater))

| Course | Area in Electricity Markets| 
|:------|:-------|
| Microeconomics | Demand-Supply Curve / Maximizing Social Welfare |
| Linear Programming (LP) | Market Clearing Pricing Optimization |
| Game Theory (Nash Equilibrium) | Alternative Market Clearing Pricing Model |
| Non-linear Programming | KKT Conditions and Lagrangian Multiplier |
| Quantitative Logistics | Electricity Transmission and Dispatch |
| Combinatorial Optimization | The U.S Market as Unit Commitment and Model Relaxation |
| Financial Derivatives | Trading Concepts of Intraday Markets and Future Markets |
| Quantitative Risk Management | CVaR (Expected Shortfall) |
| Machine Learning and AI | Forecasting Tasks |

# 🛠 Tech Stack
## Introduction
The repository provides both Python and Julia implementations as recommended in this course ([Lecture 0](https://www.youtube.com/watch?v=QmdBpKUP4Ek)**), but the focus is on Python**. 


* Note that Gurobi is a commerical / industrial-level modeling solver, and its local installation requires academic / business license; this repository provides no instruction on software installation or license-key request, please find such information via each software's official website. **For those who have difficulty acquiring a license-key to Gurobi, please smoothly change to HiGHS**.

* Gurobi and HiGHS are solvers having their own API to model the optimization problem; `pyomo` in Python and `JuMP.jl` in Julia are modeling frameworks that require necessary outside solvers.

* Mixed Complementarity Problem (MCP) requires the PATH solver.

* Links to official websites or documentations:

    🎺 [Python](https://www.python.org/)

    🎵 [Julia](https://julialang.org/)

    ♦️ [Gurobi 13.0 Documentation](https://docs.gurobi.com/current/#gurobi-version-documentation)

    ♦️ [HiGHS Documentation](https://ergo-code.github.io/HiGHS/dev/)

    ♦️ [JuMP Documentation](https://jump.dev/JuMP.jl/stable/)
    
    ♦️ [Pyomo Documentation 6.9.5](https://pyomo.readthedocs.io/en/stable/)

    ♦️ [PATH Solver](https://pages.cs.wisc.edu/~ferris/path.html)

## Python

| Dependency | Use | License Free | 
|:------|:-------|:--------:|
| `gurobipy` | LP Modeling & LP solver |❌ |
| `highspy` | LP Modeling & LP solver |✅ |
| `pyomo` | LP and MCP Modeling |✅ |
| `pandas` | Data Processing|✅ |
| `tabulate` | Visualization |✅|

## Julia

| Dependency | Use | License Free |
|:------|:-------|:--------:|
| `Gurobi.jl` | LP Modeling & LP solver |❌ |
| `HiGHS.jl` | LP Modeling & LP solver |✅ |
| `JuMP.jl` | LP and MCP Modeling |✅ |

## PATH Solver
PATH solver has multiple versions. 

Due to a technical issue in Julia (the reason has not been clear, but it seems that `PATHSolver.jl` can only solve MCPs when equalities are absent), this repository solely coveres the MCP code implementation in Python by using `pyomo` and `pathampl.exe` downloaded in [PATH Solver](https://pages.cs.wisc.edu/~ferris/path/ampl/). Please download the corresponding version under a specific operation system. (**Available for Win64, MacOS and Linux64**) 

`pathampl.exe` for Win64 has been in the project.


# 📃 Project Strucutre 
```
src/
├── assignment_1/        -> assginment 1 folder (currently empty)
├── assignment_2/        -> assginment 2 folder (currently empty)
|
├── lectures/            -> lectures folder
│   ├── Lecture_2.jl        -> code implementation for Lecture 2 by Julia
│   ├── Lecture_2.py        -> code implementation for Lecture 2 by Python
│   ├── Lecture_3.jl        -> code implementation for Lecture 3 by Julia
│   ├── Lecture_3.py        -> code implementation for Lecture 3 by Python
│   ├── Lecture_4.py        -> code implementation for Lecture 4 by Python
│   ├── Lecture_5b.jl       -> code implementation for Lecture 5b by Julia
│   ├── Lecture_5b.py       -> code implementation for Lecture 5b by Python
│   ├── Lecture_6.jl        -> code implementation for Lecture 6 by Julia
│   └── Lecture_6.py        -> code implementation for Lecture 6 by Python
|
├── .gitignore           -> git ignore file
├── main.py              -> Interface to run
├── Manifest.toml        -> Julia dependencies
├── pathampl.exe         -> PATH Solver for Win64
├── Project.toml         -> Julia dependencies
├── README.md            -> README file
└── requirements.txt     -> Python dependencies
```

# 💻 Case Study and Coding
## Summary of Lecture Cases

| Lecture Number | Focus | 
|:------:|:-------|
| 2 | Supply-Demand Curve - Social Welfare Maximization - Market Clearing Price |
| 3 | Transmission Line Constraints - Congestion Rent|
| 4 | Nash Equilibrium - Mixed Complementarity Problem |
| 5b | Balancing Market - Capacity Reserved Constraints|
| 6 | Reserve Market - A Simple Optimization throughout All Markets |
## Python Dependencies and Script Running

Python: 3.11 or versions that support the dependencies in the `requirements.txt`. Note that Jupyter Notebook not included in `requirements.txt`, please install if run any `.ipynb` files

Install dependencies:
```bash
pip install -r requirements.txt
```
Or quick installation by uv:
```bash
pip install uv
```
```bash
uv pip install -r requirements.txt
```
Run the script:

* integrated `main.py` can be selected

* one can also run independent script in lectures folder

* the only difference is `Lecture_4.py`, which is an integrated script to solve `Lecture_2.py` and `Lecture_3.py` cases by converting LP to MCP

*for example in `main.py`, by entering values in the UI, the result of case in **Lecutre 2** is shown below*:
```bash
# code
import src.lectures.Lecture_2 as l2
# import src.lectures.Lecture_3 as l3
# import src.lectures.Lecture_4 as l4
# import src.lectures.Lecture_5b as l5
# import src.lectures.Lecture_6 as l6

if __name__ == "__main__":
    l2.UI()
    
    # l3.UI()

    # MCP case for L4
    # l4.run_l2_mcp_elastic()
    # l4.run_l2_mcp_inelastic()
    # l4.run_l3_mcp()
    # l4.run_l4_mcp()
    # l4.run_l4_opt()

    # l5.UI()
    # l6.UI()
```
```
# interface in cmd or Powershell

Please enter the max demand amount (MW): 40
If inelastic, set demand price large enough, e.g., 9999
Please enter the demand price ($/MW): 40
Please enter the solver to use (gurobi/highs): highs
```
```
# optimal results

--------------------------
---- Optimal Solution ----
--------------------------
Optimal social welfare: 1200.0       
Optimal market (marginal) price: 20.0
Optimal demand amount: 40.0 MW       
Demand price: 40.0
Optimal demand total utility: 1600.0 

+------------+-------------+---------------+----------------+-----------+--------+----------+
| producer   |   supply_MW |   offer_price |   market_price |   revenue |   cost |   profit |
|------------+-------------+---------------+----------------+-----------+--------+----------|
| w1         |       20.00 |             0 |          20.00 |    400.00 |   0.00 |   400.00 |
| g1         |       20.00 |            20 |          20.00 |    400.00 | 400.00 |     0.00 |
| g2         |        0.00 |            30 |          20.00 |      0.00 |   0.00 |     0.00 |
+------------+-------------+---------------+----------------+-----------+--------+----------+
```
<!-- ## Julia Installation in VS Code (Win64)
* Install Julia

* Install Julia in VS Code Extensions

* Set Julia path to VS Code: 
    * Method 1: In VS Code -> "File" -> "Preferences" -> "Settings" -> Search Julia -> Find "Julia: Executable Path" -> Fill in the path of `julia.exe` (e.g C:\Xiaojing\julia\Julia-1.10.10\bin\julia.exe)

    * Method 2: `Ctrl` + `Shift` + `p` -> Type "settings" -> "Preferences: Open User Settings (JSON)" -> Add `"julia.executablePath": "<Path of julia.exe>",` (in `<>` fill in the path, e.g C:\Xiaojing\julia\Julia-1.10.10\bin\julia.exe) -->

## Julia Dependencies and Script Running
Activate the current directory from global env
 ```bash
Julia > import Pkg
Julia > Pkg.activate(".")
```
Install the packages required in `Project.toml`
 ```bash
Julia > Pkg.instantiate()
```
Run the script (must store the updated version first and then run)
 ```bash
Julia > include("<name of the script>")
```
*for example in Powershell activating Julia, by entering values in the UI, the result of case in **Lecutre 2** is shown below*: 

**(still note that `Lecture_4.jl` is missing due to a technical issue of `PATHSolver.jl` in Julia)**
```
(.venv) PS C:\Users\Xiaojing\PycharmProjects\DTU_renewables> julia
               _
   _       _ _(_)_     |  Documentation: https://docs.julialang.org
  (_)     | (_) (_)    |
   _ _   _| |_  __ _   |  Type "?" for help, "]?" for Pkg help.    
  | | | | | | |/ _` |  |
  | | |_| | | | (_| |  |  Version 1.10.10 (2025-06-27)
 _/ |\__'_|_|_|\__'_|  |  Official https://julialang.org/ release  
|__/                   |

julia> import Pkg as pk

julia> pk.activate(".")
  Activating project at `C:\Users\Xiaojing\PycharmProjects\DTU_renewables`

julia> include("src\\lectures\\Lecture_2.jl")
Please enter the max demand (MWh): 40
If inelastic demand, enter a very high value, eg. 9999
Please enter the demand price: 40
Optimization Successful!
Objective value: 1200.0
Optimal p_w1: 20.0
Optimal p_g1: 20.0
Optimal p_g2: 0.0 
Optimal p_d1: 40.0
Market price is: 20.0
```

# ⚖️ MIT LICENSE
This project is still ongoing and please feel free to add either new relevant content or corrections to it.
