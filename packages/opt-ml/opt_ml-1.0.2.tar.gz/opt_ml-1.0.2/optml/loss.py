import numpy as np


class Loss:
    def __init__(self, loss_fn):
        self.loss_fn = loss_fn
        self.loss = None

    def compute_loss(self, y_hat, y_true, update=False):
        if self.loss_fn == 'mse':
            loss = np.subtract(y_hat, y_true)
            cost = np.square(loss).mean()
            if update:
                self.loss = loss
            return cost
        else:
            raise NotImplementedError


class Regularization:
    def __init__(self,
                 reg,
                 reg_coeff: float = 0.0):
        self.reg = reg
        self.reg_coeff = reg_coeff

    def compute_cost(self, W):
        if self.reg == 'L1':
            return self.reg_coeff * np.linalg.norm(W, ord=1)
        elif self.reg == 'L2':
            return self.reg_coeff * np.linalg.norm(W, ord=2)
        else:
            return 0

