class KurtosisRelativaTransformer:
    def __init__(self, window=50):
        self.window = window

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        kurtosis = X["retorno_porcentaje"].rolling(window=self.window).kurt()
        pmc = kurtosis.rolling(window=self.window).min()
        X[f"Kurtosis_rel_{self.window}"] = (kurtosis - pmc) / pmc
        return X