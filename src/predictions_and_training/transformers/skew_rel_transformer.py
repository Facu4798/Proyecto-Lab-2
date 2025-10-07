class SkewRelativaTransformer:
    def __init__(self, window=50):
        self.window = window

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        skew = X["retorno_porcentaje"].rolling(window=self.window).skew()
        pmc = skew.rolling(window=self.window).min()
        X[f"Skew_rel_{self.window}"] = (skew - pmc) / pmc
        return X