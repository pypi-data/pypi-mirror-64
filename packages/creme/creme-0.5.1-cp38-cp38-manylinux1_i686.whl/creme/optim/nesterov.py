import collections

from . import base


__all__ = ['NesterovMomentum']


class NesterovMomentum(base.Optimizer):
    """Nesterov Momentum optimizer.

    Example:

        ::

            >>> from creme import datasets
            >>> from creme import linear_model
            >>> from creme import metrics
            >>> from creme import model_selection
            >>> from creme import optim
            >>> from creme import preprocessing

            >>> X_y = datasets.Phishing()
            >>> optimizer = optim.NesterovMomentum()
            >>> model = (
            ...     preprocessing.StandardScaler() |
            ...     linear_model.LogisticRegression(optimizer)
            ... )
            >>> metric = metrics.F1()

            >>> model_selection.progressive_val_score(X_y, model, metric)
            F1: 0.843668

    """

    def __init__(self, lr=0.1, rho=0.9):
        super().__init__(lr)
        self.rho = rho
        self.s = collections.defaultdict(float)

    def update_before_pred(self, w):

        for i in w:
            w[i] -= self.rho * self.s[i]

        return w

    def _update_after_pred(self, w, g):

        # Move w back to it's initial position
        for i in w:
            w[i] += self.rho * self.s[i]

        for i, gi in g.items():
            self.s[i] = self.rho * self.s[i] + self.learning_rate * gi
            w[i] -= self.s[i]

        return w
