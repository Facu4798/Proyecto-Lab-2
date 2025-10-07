class VolatilidadAjustadaTransformer:
    def __init__(self, short_window=10, long_window=50, column='retorno_porcentaje'):
        self.short_window = short_window
        self.long_window = long_window
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        var_short = X[self.column].rolling(window=self.short_window).var()
        var_long = X[self.column].rolling(window=self.long_window).var()
        X[f'Vol_{self.short_window}_adj'] = (var_short / var_long).fillna(0)
        return X