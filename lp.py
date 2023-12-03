from gurobipy import Model, GRB

m = Model("facility_location")

facility_cost = [1.1, 1]  
transport_cost = [[1, 3, 3, 3], 
                  [1, 1, 1, 1]]  


num_facilities = len(facility_cost)
num_cities = len(transport_cost[0])

x = m.addVars(num_facilities, vtype=GRB.CONTINUOUS, name="x") 
y = m.addVars(num_facilities, num_cities, vtype=GRB.CONTINUOUS, name="y") 

m.setObjective(sum(facility_cost[i] * x[i] for i in range(num_facilities)) +
               sum(transport_cost[i][j] * y[i, j] for i in range(num_facilities) for j in range(num_cities)), GRB.MINIMIZE)

for j in range(num_cities):
    m.addConstr(sum(y[i, j] for i in range(num_facilities)) == 1)

for i in range(num_facilities):
    for j in range(num_cities):
        m.addConstr(y[i, j] <= x[i])

m.optimize()

if m.status == GRB.OPTIMAL:
    print("optimal:")
    for i in range(num_facilities):
        if x[i].X > 0.5:  # 设施建设决策
            print(f"open facility {i+1}")
            for j in range(num_cities):
                if y[i, j].X > 0.5:  # 运输决策
                    print(f"  facility {i+1} city {j+1} connected")
                    
if m.status == GRB.OPTIMAL:
    print("optimal: ")
    for i in range(num_facilities):
        print(f"facility {i+1} decision: {x[i].X}")
        for j in range(num_cities):
            print(f"  facility {i+1} city {j+1} value: {y[i, j].X}")