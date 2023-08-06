from optml.model import LinModel
from optml.loss import Regularization
import numpy as np


class GradientDescent:
    def __init__(self,
                 model,
                 loss,
                 lr: float = 0.001,
                 regularization: Regularization = None):
        self.model = model
        self.w_t0 = model.W
        self.loss = loss
        self.regularization = regularization

        self.grad = self.get_sub_grad()

        w_t1 = self.w_t0 - lr * self.grad
        # update model
        model.W = w_t1

    def get_sub_grad(self):
        if self.regularization is None:
            return self.get_sub_grad_loss()
        else:
            return self.get_sub_grad_loss() + self.regularization.reg_coeff * self.get_sub_grad_reg()

    def get_sub_grad_loss(self):
        if type(self.model) is LinModel:
            if self.loss.loss_fn == 'mse':
                # # We are solving the 1/2||XW - Y||^2
                # # This is differentiable and sub - diff is (X^T * X * W - X^T * Y) = X^T(y_hat - y_true)
                x = self.model.X
                m = len(x)
                x_transpose = x.transpose()
                grad_w = np.dot(x_transpose, self.loss.loss) * (2 / m)
                return grad_w
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    def get_sub_grad_reg(self):
        if self.regularization.reg == 'L1':
            sub_grad = np.sign(self.w_t0)
            return sub_grad
        elif self.regularization.reg == 'L2':
            sub_grad = 2 * self.w_t0
            return sub_grad
        else:
            raise NotImplementedError

