class CloseRelativoTransformer:
    def __init__(self, windows=[25, 50, 200], column='Close'):
        self.windows = windows
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for w in self.windows:
            rolling_mean = X[self.column].rolling(window=w).mean()
            X[f"{self.column}_rel_{w}"] = ((X[self.column] - rolling_mean) / rolling_mean).fillna(0)
        return X