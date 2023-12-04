from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import BinaryQuadraticModel


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
    
    return total_cost


def solve_anneal(f,c,P):
    m = len(f)
    n = len(c[0])
    bqm = BinaryQuadraticModel('BINARY')


    for i in range(m):
        bqm.add_variable(f'x_{i}', f[i])
        for j in range(n):
            bqm.add_variable(f'y_{i}_{j}', c[i][j])

    for j in range(n):
        y_vars = [f'y_{i}_{j}' for i in range(m)]
        

        for var in y_vars:
            bqm.set_linear(var, bqm.get_linear(var) - 2 * P)
        for i in range(m):
            for k in range(i + 1, m):
                bqm.add_interaction(y_vars[i], y_vars[k], 2 * P)
        bqm.offset += P  
        
    for i in range(m):
        for j in range(n):
            y_var = f'y_{i}_{j}'
            x_var = f'x_{i}'
            bqm.add_interaction(y_var, x_var, -2 * P)
            bqm.set_linear(y_var, bqm.get_linear(y_var) + P)
            bqm.set_linear(x_var, bqm.get_linear(x_var) + P)
            bqm.offset += P  

    sampler = EmbeddingComposite(DWaveSampler())

    solution = sampler.sample(bqm, num_reads=100).first.sample

    # print("Solution:", solution)
    ans = list(solution.values())
    return ans 
    
if __name__ == "__main__":
    f =  [1, 1]
    c =[[1,3,3,3,3,3,3,3,3,3], [1,1,1,1,1,1,1,1,1,1]]
    a = solve_anneal(f ,c,10)
    print(a)
    print(calculate_cost(f,c,a))
    