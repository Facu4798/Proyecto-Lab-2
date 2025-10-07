class retornosTransformer:

    def __init__(self,days=[5,10]):
        self.days = days
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        for d in self.days:
            X[f"retorno_porcentaje_{d}"] = X["retorno_porcentaje"].shift(d)
        return X