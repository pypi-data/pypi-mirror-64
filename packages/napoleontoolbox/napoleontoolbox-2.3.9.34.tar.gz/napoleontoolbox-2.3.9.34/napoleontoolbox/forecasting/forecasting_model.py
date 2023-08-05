import lightgbm as lgb
class ForecasterWrapper:
    """ Base object to roll a neural network model.
    Rolling over a time axis with a train period from `t - n` to `t` and a
    testing period from `t` to `t + s`.
    Parameters
    ----------
    X, y : array_like
        Respectively input and output data.
    f : callable, optional
        Function to transform target, e.g. ``torch.sign`` function.
    index : array_like, optional
        Time index of data.
    Methods
    -------
    __call__
    Attributes
    ----------
    n, s, r : int
        Respectively size of training, testing and rolling period.
    b, e, T : int
        Respectively batch size, number of repass_steps and size of entire dataset.
    t : int
        The current time period.
    y_eval, y_test : np.ndarray[ndim=1 or 2, dtype=np.float64]
        Respectively evaluating (or training) and testing predictions.
    """
    def __init__(self, method = 'standard'):
        """ Initialize shape of target. """
        if method == 'standard':
            self.model  = lgb.LGBMRegressor(boosting_type='gbdt', num_leaves=31, max_depth=7, learning_rate=0.05, n_estimators=100)
    def fit(self, X_train, y_train, X_val, y_val, method = 'standard'):
        if method == 'standard':
            self.model.fit(X_train, y_train,
        eval_set=[(X_val, y_val)],
        eval_metric= ['l1','l2'],
        early_stopping_rounds=5,
        verbose= 0)
    def predict(self, X_test, method = 'standard'):
        if method == 'standard':
            y_pred = self.model.predict(X_test)
            return y_pred
        return None