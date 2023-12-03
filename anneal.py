from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import BinaryQuadraticModel

m = 2  
n = 4  
f = [1.1, 1] 
c = [[1,3,3,3], [1,1,1,1]] 
P = 10  


bqm = BinaryQuadraticModel('BINARY')


for i in range(m):
    bqm.add_variable(f'x_{i}', f[i])
    for j in range(n):
        bqm.add_variable(f'y_{i}{j}', c[i][j])

for j in range(n):
    y_vars = [f'y_{i}{j}' for i in range(m)]
    

    for var in y_vars:
        bqm.set_linear(var, bqm.get_linear(var) - 2 * P)
    for i in range(m):
        for k in range(i + 1, m):
            bqm.add_interaction(y_vars[i], y_vars[k], 2 * P)
    bqm.offset += P  
    
for i in range(m):
    for j in range(n):
        y_var = f'y_{i}{j}'
        x_var = f'x_{i}'
        bqm.add_interaction(y_var, x_var, -2 * P)
        bqm.set_linear(y_var, bqm.get_linear(y_var) + P)
        bqm.set_linear(x_var, bqm.get_linear(x_var) + P)
        bqm.offset += P  

sampler = EmbeddingComposite(DWaveSampler())

solution = sampler.sample(bqm, num_reads=100).first.sample

print("Solution:", solution)