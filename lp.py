from gurobipy import Model, GRB



def solve_lp(facility_cost,transport_cost):
    
    num_facilities = len(facility_cost)
    num_cities = len(transport_cost[0])
    res = [0]*(num_facilities+num_cities*num_facilities)
    m = Model("facility_location")
    m.setParam("OutputFlag", 0)
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
        # print("optimal:")
        for i in range(num_facilities):
            if x[i].X > 0.5:  
                # print(f"open facility {i+1}")
                res[i] = 1
                for j in range(num_cities):
                    if y[i, j].X > 0.5:  
                        # print(f"  facility {i+1} city {j+1} connected")
                        res[num_facilities+i*num_cities+j] = 1
    return res
if __name__ == "__main__": 
    facility_cost = [1.1, 1]  
    transport_cost = [[1, 3, 3, 3], 
                  [1, 1, 1, 1]]  
    print(solve_lp(facility_cost,transport_cost))