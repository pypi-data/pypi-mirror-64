import numpy as np


class WeightInitialization:
    def __init__(self, in_dim: int,
                 out_dim: int,
                 initialization: str = 'random'):
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.init = initialization

    def get_wt(self):
        if self.init == 'random':
            w = np.random.rand(self.in_dim, self.out_dim)
            return w
        elif self.init == 'zeros':
            w = np.zeros((self.in_dim, self.out_dim))
            return w
        else:
            raise NotImplementedError
