import math

from .. import base


__all__ = ['TransformedTargetRegressor', 'BoxCoxRegressor']


class TransformedTargetRegressor(base.Regressor, base.Wrapper):
    """Modifies the target before training.

    The user is expected to check that ``func`` and ``inverse_func`` are coherent with each other.

    Parameters:
        regressor (creme.base.Regressor): regressor model applied for training.
        func (callable): a function modifying the target before training.
        inverse_func (callable): a function to return to the target's original space.

    Example:

        ::

            >>> import math
            >>> from creme import datasets
            >>> from creme import linear_model
            >>> from creme import meta
            >>> from creme import metrics
            >>> from creme import model_selection
            >>> from creme import preprocessing

            >>> X_y = datasets.TrumpApproval()
            >>> model = (
            ...     preprocessing.StandardScaler() |
            ...     meta.TransformedTargetRegressor(
            ...         regressor=linear_model.LinearRegression(intercept_lr=0.15),
            ...         func=math.log,
            ...         inverse_func=math.exp
            ...     )
            ... )
            >>> metric = metrics.MSE()

            >>> model_selection.progressive_val_score(X_y, model, metric)
            MSE: 8.970517

    """

    def __init__(self, regressor, func, inverse_func):
        self.regressor = regressor
        self.func = func
        self.inverse_func = inverse_func

    @property
    def _model(self):
        return self.regressor

    def fit_one(self, x, y):
        self.regressor.fit_one(x, self.func(y))
        return self

    def predict_one(self, x):
        y_pred = self.regressor.predict_one(x)
        return self.inverse_func(y_pred)


class BoxCoxRegressor(TransformedTargetRegressor):
    """Applies the Box-Cox transform to the target before training.

    Box-Cox transform is useful when the target variable is heteroscedastic (i.e. there are
    sub-populations that have different variabilities from others) allowing to transform it towards
    normality.

    The ``power`` parameter is denoted λ in the litterature. If ``power`` is equal to 0 than the
    Box-Cox transform will be equivalent to a log transform.

    Parameter:
        regressor (creme.base.Regressor): regressor model applied for training.
        power (float): power value to do the transformation.

    Example:

        ::

            >>> import math
            >>> from creme import datasets
            >>> from creme import linear_model
            >>> from creme import meta
            >>> from creme import metrics
            >>> from creme import model_selection
            >>> from creme import preprocessing

            >>> X_y = datasets.TrumpApproval()
            >>> model = (
            ...     preprocessing.StandardScaler() |
            ...     meta.BoxCoxRegressor(
            ...         regressor=linear_model.LinearRegression(intercept_lr=0.2),
            ...         power=0.05
            ...     )
            ... )
            >>> metric = metrics.MSE()

            >>> model_selection.progressive_val_score(X_y, model, metric)
            MSE: 6.003676

    """

    def __init__(self, regressor, power=1.):
        super().__init__(
            regressor=regressor,
            func=(lambda y: (y ** power - 1) / power) if power > 0 else math.log,
            inverse_func=(lambda y: (power * y + 1) ** (1 / power)) if power > 0 else math.exp
        )
