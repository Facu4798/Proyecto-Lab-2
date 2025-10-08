class atrTransformer:
    def __init__(self,window=14):
        self.window = window
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X = X.copy()
        import numpy as np
        X['H-L'] = X['High'] - X['Low']
        X['H-PC'] = np.abs(X['High'] - X['Close'].shift(1))
        X['L-PC'] = np.abs(X['Low'] - X['Close'].shift(1))
        X['TR'] = X[['H-L', 'H-PC', 'L-PC']].max(axis=1)
        X['ATR'] = X['TR'].rolling(window=self.window).mean()
        X.drop(['H-L', 'H-PC', 'L-PC', 'TR'], axis=1, inplace=True)
        return X