from sklearn import svm
from MFCCStuff import *


class SVMStuff:
    # 22 according to paper (https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.148.5904&rep=rep1&type=pdf)
    order = 22

    def __init__(self, target_x, impostor_x):
        self.target_num_rows, self.target_num_cols = target_x.shape
        self.impostor_num_rows, self.impostor_num_cols = impostor_x.shape

        self.target_x = target_x
        self.target_y = [1] * self.target_num_rows

        self.impostor_x = impostor_x
        self.impostor_y = [-1] * self.impostor_num_rows

        self.svm = None  # Support vector machine
        self.fit_model()

    def fit_model(self):
        self.svm = svm.SVC(kernel="rbf", gamma='scale', decision_function_shape='ovr')
        x = np.concatenate((self.target_x, self.impostor_x), axis=0)
        y = self.target_y + self.impostor_y
        self.svm.fit(x, y)

    def predict(self, impostor_x):
        return self.svm.predict(impostor_x)



