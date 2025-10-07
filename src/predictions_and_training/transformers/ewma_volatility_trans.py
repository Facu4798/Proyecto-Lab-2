class ewmaVolatilityTransformer:
    def __init__(self,span=20):
        self.span = span
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X = X.copy()
        X["EWMA_Volatility"] = X["retorno"].ewm(span=self.span,adjust=False).std()
        return X