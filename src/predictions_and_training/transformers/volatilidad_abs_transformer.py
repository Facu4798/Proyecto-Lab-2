class VolatilidadAbsolutaTransformer:
    def __init__(self, window=5, column='retorno_porcentaje'):
        self.window = window
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        import numpy as np
        X = X.copy()
        X[f'Abs_Var_{self.window}d'] = X[self.column].rolling(window=self.window).apply(
            lambda x: np.abs(x[-1] - x[0]),
            raw=True
        ).fillna(0)
        return X