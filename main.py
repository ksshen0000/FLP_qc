import lp
import cqm
import anneal
import random
def calculate_cost(facility_cost,transport_cost,sol):
    num_facilities = len(facility_cost)
    num_cities = len(transport_cost[0])
    total_cost=0
    for i in range(num_facilities):
        if sol[i]==1:
            total_cost+=facility_cost[i]
            for j in range(num_cities):
                if sol[num_facilities+i*num_cities+j]==1:
                    total_cost+= transport_cost[i][j]
    for j in range(num_cities):
        s = 0
        for i in range(num_facilities):
            if sol[i] == 1 and sol[num_facilities+i*num_cities+j]==1:
                s+=1
        if s==0 :
            return False
    return total_cost


if __name__ == "__main__":
    for i in range(10):
        num_cities = (i+1)*4
        num_facilities = (i+1)*2
        facility_cost = [random.randint(5, 10) for _ in range(num_facilities)]
        transport_cost = [[random.randint(5, 10) for _ in range(num_cities)] for _ in range(num_facilities)]
        # print(transport_cost)
        lp_res = calculate_cost(facility_cost,transport_cost,lp.solve_lp(facility_cost,transport_cost))
        # neal_res  = calculate_cost(facility_cost,transport_cost,anneal.solve_anneal(facility_cost,transport_cost,500))
        cqm_res = calculate_cost(facility_cost,transport_cost,cqm.solve_cqm(facility_cost,transport_cost))
        
        print(num_facilities,num_cities)
        print(lp_res,cqm_res)
