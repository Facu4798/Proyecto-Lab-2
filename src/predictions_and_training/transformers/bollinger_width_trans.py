class bollingerWidthTransformer:
    def __init__(self,window=20,num_std=2):
        self.window = window
        self.num_std = num_std
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X = X.copy()
        rolling_mean = X['Close'].rolling(window=self.window).mean()
        rolling_std = X['Close'].rolling(window=self.window).std()
        X['Bollinger_Width'] = (rolling_std * self.num_std * 2) / rolling_mean
        return X