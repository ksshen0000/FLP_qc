from dimod import ConstrainedQuadraticModel, Binary
from dwave.system import LeapHybridCQMSampler


def solve_cqm(facility_cost,service_cost):
    num_facilities = len(facility_cost)
    num_customers = len(service_cost[0])
    # print(num_facilities,num_customers)
    cqm = ConstrainedQuadraticModel()

    facilities = [Binary(f'x{i}') for i in range(num_facilities)]
    customers = [[Binary(f'y_{i}_{j}') for j in range(num_customers)] for i in range(num_facilities)]
    objective = sum(facility_cost[i] * facilities[i] for i in range(num_facilities))
    for i in range(num_facilities):
        for j in range(num_customers):
            objective += service_cost[i][j] * customers[i][j]
    cqm.set_objective(objective)
    # 添加约束：每个客户必须被至少一个设施服务
    for j in range(num_customers):
        cqm.add_constraint(sum(customers[i][j] for i in range(num_facilities)) >= 1, label=f'customer{j}')

    # 添加额外约束：如果客户 j 由设施 i 服务，则设施 i 必须是开放的
    for i in range(num_facilities):
        for j in range(num_customers):
            cqm.add_constraint(customers[i][j] - facilities[i]<=0, label=f'facility{i}_customer{j}')

    # 使用D-Wave的CQM求解器求解问题
    sampler = LeapHybridCQMSampler()
    sampleset = sampler.sample_cqm(cqm)
    sampleset = sampleset.filter(lambda d: d.is_feasible)

    # 输出具有最低能量的解
    best_sample = sampleset.first.sample
    res = list(best_sample.values())
    res= list(map(round, res))
    return res
    
    
    
if __name__ == "__main__":
    facility_cost = [1,1]  # 各设施的开设成本
    service_cost = [  # 服务成本矩阵，service_cost[i][j] 是设施 i 服务客户 j 的成本
    [1,3,3,3],
    [1,1,1,1]]
    print(solve_cqm(facility_cost,service_cost))
    