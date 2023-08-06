import torchvision.datasets as datasets
from sklearn.preprocessing import OneHotEncoder
import numpy as np


class DataReader:
    def __init__(self, data_set='MNIST', flatten=False):
        self.data_set = data_set
        self.X_train, self.Y_train, self.X_test, self.Y_test = self.read_data(flatten=flatten)

    def read_data(self, flatten):
        if self.data_set == 'MNIST':
            return self.read_mnist(flatten)
        else:
            raise NotImplementedError

    @staticmethod
    def read_mnist(flatten):
        mnist_train = datasets.MNIST(root='./Data', download=True, train=True)
        mnist_test = datasets.MNIST(root='./Data', download=True, train=False)
        x_train = mnist_train.train_data.numpy().reshape(60000, 784).astype(np.float32)
        y_train = mnist_train.train_labels.numpy().reshape(60000, 1).astype(np.float32)
        x_test = mnist_test.train_data.numpy().reshape(10000, 784).astype(np.float32)
        y_test = mnist_test.train_labels.numpy().reshape(10000, 1).astype(np.float32)

        if flatten:
            # flatten out image
            onehot_encoder = OneHotEncoder(sparse=False, dtype=float)
            y_train = onehot_encoder.fit_transform(y_train)
            y_test = onehot_encoder.fit_transform(y_test)

        return x_train, y_train, x_test, y_test


if __name__ == '__main__':
    data_reader = DataReader(data_set='MNIST')
    print('Testing Mnist reader')
