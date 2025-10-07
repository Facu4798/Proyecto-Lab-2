class VolatilidadRelativaTransformer:
    def __init__(self, windows=[25, 50, 200], column='retorno_porcentaje'):
        self.windows = windows
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for w in self.windows:
            vol = X[self.column].rolling(window=w).std()
            max_vol = vol.rolling(window=w).max()
            X[f"Var_rel_{w}"] = ((vol - max_vol) / max_vol).fillna(0)
        return X