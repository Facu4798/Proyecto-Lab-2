class RSITRansformer:

    def __init__(self, window=14):
        self.window = window

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        
        delta = X['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=self.window).mean()
        avg_loss = loss.rolling(window=self.window).mean()

        rs = avg_gain / avg_loss
        X['RSI'] = 100 - (100 / (1 + rs))

        return X
