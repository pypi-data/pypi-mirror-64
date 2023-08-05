from napoleontoolbox.rebalancing import rolling
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import pandas as pd

def rolling_forecasting(forecasting_model, X, y, n=252, s=63, s_eval= None, method = 'standard', display = False, **kwargs):
    assert X.shape[0] == y.shape[0]
    idx = X.index
    forecasting_series = pd.Series(index=idx, name='prediction')

    if n is None and s_eval is None:
        roll = rolling._ExpandingRollingMechanism(idx, s=s)
    if n is None and s_eval is not None:
        roll = rolling._ExpandingEvalRollingMechanism(idx, s=s, s_eval = s_eval)
    if n is not None and s_eval is None :
        roll = rolling._RollingMechanism(idx, n=n, s=s)
    if n is not None and s_eval is not None:
        roll = rolling._EvalRollingMechanism(idx, n=n, s=s, s_eval = s_eval)

    for slice_n, slice_s, slice_s_eval in roll():
        # Select X
        X_train = X.loc[slice_n].copy()
        y_train = y.loc[slice_n].copy()

        X_test = X.loc[slice_s].copy()
        y_test = y.loc[slice_s].copy()

        forecasting_model.fit(X_train, y_train, method)
        y_pred = forecasting_model.predict(X_test, method)
        forecasting_series.loc[slice_s] = y_pred

        matrix = confusion_matrix(y_test > 0, y_pred > 0)
        rmse = mean_squared_error(y_test, y_pred)
        accuracy = accuracy_score(y_test > 0, y_pred > 0)

        if display:
            print('training slice ' + str(slice_n))
            print('testing slice ' + str(slice_s))
            print('rmse for slice : '+str(rmse))
            print('accuracy')
            print(accuracy)
            print('confusion matrix')
            print(matrix)

    return forecasting_series

