from .base import BaseModel
import numpy as np



class KNeighborsClassifier(BaseModel):
    def __init__(self, k=3, p=2):
        super(KNeighborsClassifier, self).__init__()
        self.k = k
        self.p = p
        self.X = None
        self.y = None


    def fit(self, X, y):
        self.X = X
        self.y = y
        super(KNeighborsClassifier, self).fit()


    def calc_dist(self, x1, x2):
        if x1.ndim == 1:
            x1 = np.expand_dims(x1, axis=0)
        if x2.ndim == 1:
            x2 = np.expand_dims(x2, axis=0)
        dist = np.power(np.sum(np.abs(x1 - x2) ** self.p, axis=1, keepdims=True), 1 / self.p)
        return dist


    def predict(self, X):
        dist = self.calc_dist(X, self.X)
        closet_index = np.argsort(dist, axis=0)[:self.k]
        closet_label = self.y[closet_index]
        majority_label = self.counter(closet_label)
        return majority_label

    def counter(self, label_list):
        label_dict = {}

        for label in label_list:
            if label[0] not in label_dict.keys():
                label_dict[label[0]] = 0
            else:
                label_dict[label[0]] += 1
        majority_label_count = 0
        majority_label = label_list[0]
        for label, count in label_dict.items():
            if count > majority_label_count:
                majority_label_count = count
                majority_label = label
        return majority_label


    def score(self, X, y, reduction='mean'):
        pred = np.zeros_like(y)
        for i in range(X.shape[0]):
            pred[i] = self.predict(X[i])

        if reduction == 'mean':
            acc = np.mean(pred == y)
        else:
            acc = np.sum(pred == y)
        print('accuracy on test data is ', acc)
        return acc

