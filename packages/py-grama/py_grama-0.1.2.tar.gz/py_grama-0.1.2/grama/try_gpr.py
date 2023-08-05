from sklearn.datasets import make_friedman2
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel, RBF

X, y = make_friedman2(n_samples=500, noise=0, random_state=0)
kernel = DotProduct() + WhiteKernel()
gpr = GaussianProcessRegressor(
    # kernel=kernel,
    kernel=RBF(),
    random_state=0
).fit(X, y)

print(gpr.score(X, y))
print(gpr.predict(X[:2,:], return_std=True))
param_str = str(gpr.get_params())
print(param_str)
