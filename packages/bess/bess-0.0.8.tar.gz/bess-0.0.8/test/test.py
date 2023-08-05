import numpy as np
from bess.linear import PdasLm, PdasLogistic, PdasPoisson

np.random.seed(12345)
x = np.random.normal(0, 1, 100 * 150).reshape((100, 150))
beta = np.hstack((np.array([1, 1, -1, -1, -1]), np.zeros(145)))
noise = np.random.normal(0, 1, 100)
y = np.matmul(x, beta) + noise
print(x[:3, :6])
print(beta[:10])
print(y[:3])
model = PdasLm(path_type="seq", sequence=[5])
model.fit(X=x, y=y)
print(np.nonzero(model.beta))
print(model.beta[:10])

np.random.seed(12345)
x = np.random.normal(0, 1, 100 * 150).reshape((100, 150))
beta = np.hstack((np.array([1, 1, -1, -1, -1]), np.zeros(145)))
xbeta = np.matmul(x, beta)
p = np.exp(xbeta)/(1+np.exp(xbeta))
y = np.random.binomial(1, p)
print(x[:3, :6])
print(beta[:10])
print(y[:3])
model = PdasLogistic(path_type="seq", sequence=[5])
model.fit(X=x, y=y)
print(np.nonzero(model.beta))
print(np.nonzero(model.beta))
print(model.beta[:10])

np.random.seed(12345)
x = np.random.normal(0, 1, 100 * 150).reshape((100, 150))
beta = np.hstack((np.array([1, 1, -1, -1, -1]), np.zeros(145)))
lam = np.exp(np.matmul(x, beta))
y = np.random.poisson(lam=lam)
print(x[:3, :6])
print(beta[:10])
print(y[:3])
model = PdasPoisson(path_type="seq", sequence=[5])
model.fit(x, y)
print(np.nonzero(model.beta))
print(model.beta[:5])



