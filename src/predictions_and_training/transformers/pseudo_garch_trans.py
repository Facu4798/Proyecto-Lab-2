class pseudoGarchTransformer:
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    def transform(self,X):
        X=X.copy()
        X['RollingShock_10'] = (X['retorno_porcentaje'] - X['retorno_porcentaje'].rolling(window=2).mean())**2
        X['RollingShock_10'] = X['RollingShock_10'].rolling(window=10).mean()
        return X