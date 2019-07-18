from gurobipy import *
import numpy as np
import pandas as pd
import random
import xlrd


def optimize(F,f,w,W,c,E,mu,a,a1,k,N,M):

    model = Model()
    z = model.addVars(a,vtype=GRB.BINARY)
    x = model.addVars(a,k,vtype=GRB.BINARY)
    #y = model.addVar(ub = 1.0, lb= 0.0,vtype= GRB.INTEGER)

    obj = quicksum(F[i,j]*z[i,j] for i, j in a) + quicksum(c[i,j,g,h,t] * x[i,j,g,h,t] for i,j in a for g,h,t in k) + mu * quicksum(quicksum(f[g,h,t]*(x[i,j,g,h,t]-x[j,i,g,h,t])*(x[i,j,g,h,t]-x[j,i,g,h,t]) for g,h,t in k) for i,j in a1)

    model.setObjective(obj,GRB.MINIMIZE)

    ind = {}
    for i in N:
        for g,h,t in k:
            if i == g:
                tmp = -1
            else:
                if i == h:
                    tmp = 1
                else:
                    tmp = 0
            ind.update({(i, g, h, t): tmp})
    print(E[2])
    loc = {}
    for i in N:
        tmp = 0
        for g,h,t in k:
            if g == i:
                tmp += f[g,h,t]
        loc.update({i: tmp})

    middle_var = model.addVars(a)


    model.addConstrs((quicksum(x[j,i,g,h,t] for j,i in a.select('*',i))-quicksum(x[i,j,g,h,t] for i,j in a.select(i,'*')) == ind[i,g,h,t] ) for i in N for g,h,t in k)
    model.addConstrs((x[i,j,g,h,t] <= z[i,j])for i,j in a for g,h,t in k)
    model.addConstrs((quicksum(w[i,j,g,h,t,m] * x[i,j,g,h,t] for i,j in a) <= W[g,h,t,m]) for g,h,t in k for m in M)
    model.addConstrs(middle_var[i,j] == quicksum(f[g,h,t]*x[i,j,g,h,t] for g,h,t in k) for i,j in a)
    model.addConstrs(((quicksum(middle_var[i,j] for i,j in a.select('*',j))) <= E[j] - loc[j]) for j in N)
    model.setParam('TimeLimit',72000)
    model.setParam('MIPGap',0.01)
    model.setParam('FlowCoverCuts',2)
    model.setParam('CoverCuts',2)
    model.setParam('CliqueCuts',2)
    model.setParam('FlowPathCuts',2)
    model.setParam('NetworkCuts',1)

    model.optimize()

    val_x = model.getAttr('x',x)
    val_z = model.getAttr('x',z)

    return val_x, val_z


def opt_solve():
    Name = ['鄂尔多斯','武汉','昆明','重庆','深圳','上海','贵阳','北京','衡州','廊坊','菏泽','威海','承德','厦门','张家界','宜兴','北海','西安','长春']

    num = 10
    N = range(num)

    a = []
    k = []
    Distance = pd.read_excel('./DataSet/distance_matrix.xlsx', sheet_name='Sheet', header=None)
    Distance = np.array(Distance)

    for i in N:
        for j in N:
            if i != j:
                a.append((i,j))

    for i in N:
        for j in N:
            for tmp in range(2):
                if random.random() > 0.7 and i != j:
                    k.append((i,j,tmp))

    F_factor = np.random.uniform(10,12,(num,num))
    F = Distance[0:10,0:10] @ F_factor
    f = np.random.uniform(30,130,(num,num,2))
    c = np.zeros((num,num,num,num,2))
    for i in range(num):
        for j in range(num):
            for g in range(num):
                for h in range(num):
                    for t in range(2):
                        c[i,j,g,h,t] = random.uniform(0.095,0.105) * Distance[i,j] * f[g,h,t]




    mu = 0.005
    M = range(1)

    E = np.sum(f) * np.random.uniform(0.85,1,num)
    for i in range(num):
        for j in range(num):
            for t in range(2):
                c[i,j,t] = c[i,j,t] * f[i,j,t]
    W = np.zeros((num,num,2,1))
    w = np.zeros((num,num,num,num,2,1))

    for i in range(num):
        for j in range(num):
            for t in range(2):
                for m in range(1):
                    W[i,j,t,m] = Distance[i,j] * random.uniform(3.3,3.7)
                    for g in range(num):
                        for h in range(num):
                            w[g,h,i,j,t,m] = Distance[i,j] * random.uniform(0.9,1.1)

    a1 = [a[1],a[4],a[9],a[12],a[15],a[18]]
    a = tuplelist(a)

    val_x,val_z = optimize(F,f,w,W,c,E,mu,a,a1,k,N,M)
    return dict(val_x)

# a = list(val_x.keys())
# print(val_x[a[1]])

# if __name__ == '__main__':
#     a = opt_solve()
#     b = list(a.keys())
#     print(b[1][1])
