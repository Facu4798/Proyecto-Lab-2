class shocksPasadosTransformer:
    def __init__(self):
        pass
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X = X.copy()
        X["SquaredRet_1d"] = X["retorno_porcentaje"].shift(1)**2
        X["AbsRet_1d"] = X["retorno_porcentaje"].shift(1).abs()
        return X