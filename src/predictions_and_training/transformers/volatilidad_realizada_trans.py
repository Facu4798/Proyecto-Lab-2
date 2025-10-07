class volatilidadRealizadaTransformer:
    def __init__(self):
        pass
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X = X.copy()
        X["RealVol_5d"] = X["retorno_porcentaje"].rolling(5).std()
        X["RealVol_20d"] = X["retorno_porcentaje"].rolling(20).std()
        return X