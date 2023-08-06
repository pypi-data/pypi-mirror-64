from optml.optimizers import GradientDescent
from optml.loss import Regularization, Loss
from sklearn.utils import shuffle
import tqdm
import matplotlib.pyplot as plt


def get_batch(data, batch_size: int, start_ix: int):
    """ given a start ix and batch size this will return truncated data(list) as batch """
    if len(data) == 0:
        return []
    return data[start_ix:] if len(data[start_ix:]) <= batch_size else data[start_ix: start_ix + batch_size]


def get_lr(lr0,
           schedule):
    if schedule == 'decay':
        return lr0 * 0.999
    else:
        return lr0


def train(_model,
          x_train,
          y_train,
          x_test,
          y_test,
          loss_criterion: Loss,
          reg: Regularization = None,
          epochs=100,
          _lr=0.001,
          batch_size=None,
          _lr_schedule=None):

    train_loss = []
    test_loss = []

    if batch_size is None:
        bs = len(x_train)
    else:
        bs = batch_size
    lr = []
    passes = 0
    # train model / no_of_epoch gradient steps
    for epoch in tqdm.tqdm(range(epochs)):
        x_train, y_train = shuffle(x_train, y_train)
        iterations = len(x_train)/float(bs)

        for start_ix in range(0, len(x_train), bs):
            lr.append(_lr)
            x_batch = get_batch(data=x_train, start_ix=start_ix, batch_size=bs)
            y_batch = get_batch(data=y_train, start_ix=start_ix, batch_size=bs)

            # Do a forward prop
            # compute loss  (y_hat - y_true)
            # note the ** Update = True **
            y_hat_train = _model.forward(inp=x_batch, update=True)
            train_cost = loss_criterion.compute_loss(y_hat=y_hat_train, y_true=y_batch, update=True)
            if reg is not None:
                train_cost = train_cost + reg.compute_cost(W=_model.W)

            # if passes % 100 == 0:
            # Do a forward Prop and compute loss
            # compute test loss : note the ** Update=False **
            y_hat_test = _model.forward(inp=x_test, update=False)
            test_cost = loss_criterion.compute_loss(y_hat=y_hat_test, y_true=y_test, update=False)
            if reg is not None:
                test_cost = test_cost + reg.compute_cost(W=_model.W)

            train_loss.append(train_cost)
            test_loss.append(test_cost)

            print('\n Train Loss =', train_cost)
            print('Test Loss =', test_cost)

            # compute one step of grad descent
            GradientDescent(model=_model,
                            loss=loss_criterion,
                            regularization=reg,
                            lr=_lr)
            if _lr_schedule is not None:
                _lr = get_lr(_lr, schedule=_lr_schedule)
            passes += 1

    plt.plot(train_loss, 'b-')
    plt.plot(test_loss, 'g--')
    plt.show()
    plt.plot(lr, color='r', marker='o', linestyle='dashed')
    plt.show()
