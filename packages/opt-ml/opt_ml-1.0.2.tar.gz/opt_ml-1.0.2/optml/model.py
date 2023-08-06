from optml.initialization import WeightInitialization
import numpy as np


class LinModel:
    def __init__(self,
                 dim_in: int,
                 dim_out: int,
                 bias=True,
                 init='random'):
        self.bias = bias
        self.X = None
        if bias:
            self.W = WeightInitialization(in_dim=dim_in + 1,
                                          out_dim=dim_out,
                                          initialization=init).get_wt()
        else:
            self.W = WeightInitialization(in_dim=dim_in,
                                          out_dim=dim_out,
                                          initialization=init).get_wt()

    def forward(self, inp, update=False):
        # return XW basically
        if self.bias:
            x_ones = np.ones((inp.shape[0], 1))
            inp = np.append(inp, x_ones, 1)
        if update:
            self.X = inp
        op = np.matmul(inp, self.W)
        return op
