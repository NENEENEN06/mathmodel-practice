import numpy as np

n = eval(input("请输入参评数目："))
m = eval(input("请输入指标数目："))
kinds = input("请输入类型矩阵：1：极大型 2：极小型 3：中间型 4：区间型\n").split(" ")

print("请输入矩阵：")
A = np.zeros((n,m))

for i in range(n):
    A[i] = input().split()
    A[i] = list(map(float, A[i]))
print("输入矩阵为：\n{}".format(A))
# 90 4 35 15
# 85 3 50 21
# 92 4.5 40 19
#88 3.5 38 17

def minTomax(maxx,x):
    x = list(x)
    ans = [[maxx-e] for e in x]
    return np.array(ans)

def midTomax(bestx, x):
    x = list(x)
    h = [abs(e-bestx) for e in x]
    M = max(h)
    if M==0:
        M=1
    ans = [[1-e/M] for e in h]
    return np.array(ans)

def regTomax(lowx, highx, x):
    x=list(x)
    M = max(lowx-min(x), max(x)-highx)
    if M==0:
        M=1
    ans=[]
    for e in x:
        if e<lowx:
            ans.append([(1-(lowx-e)/M)])
        elif e>highx:
            ans.append([(1-(e-highx)/M)])
        else:
            ans.append([1])
    return np.array(ans)

X = np.zeros(shape=(n,1))

for i in range(m):
    if kinds[i]=="1":
        v = np.array(A[:,i])
    elif kinds[i]=="2":
        maxA = max(A[:,i])
        v = minTomax(maxA, A[:,i])
    elif kinds[i]=="3":
        bestA = eval(input("类型三：请输入最优值"))
        v = midTomax(bestA, A[:, i])
    elif kinds[i]=='4':
        lowA = eval(input("类型四：请输入区间[a，b]值a："))
        highA = eval(input("类型四：请输入区间[a，b]值b："))
        v = regTomax(lowA, highA, A[:, i])
    
    if i==0:
        X = v
    else:
        X = np.column_stack((X, v))

print("统一指标后矩阵为：\n{}".format(X))
X = X.astype('float')
for i in range(m):
    X[:,i] = X[:,i]/np.sqrt(sum(X[:,i]**2))
print("标准化后矩阵为：\n{}".format(X))

w = list(map(float, input("请输入权重向量：").split()))
print("权重向量为：\n{}".format(w))

x_max = np.max(X, axis=0)
x_min = np.min(X, axis=0)
w = np.array(w)
d_z = np.sqrt(np.sum(w * np.square((X - np.tile(x_max, (n,1)))), axis=1))
d_f = np.sqrt(np.sum(w * np.square((X - np.tile(x_min, (n,1)))), axis=1))
print("每个指标的最大值：",x_max)
print("每个指标的最小值：",x_min)
print("d+向量：",d_z)
print("d-向量：",d_f)

s = d_f/(d_z + d_f)
for i in range(n):
    print("方案 {} 的得分为：{}".format(i+1, s[i]))