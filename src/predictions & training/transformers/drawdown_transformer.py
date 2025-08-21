class DrawdownTransformer:
    def __init__(self, window=30):
        self.window = window

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        import numpy as np
        X = X.copy()
        close = X['Close'].values
        drawdowns = []

        for i in range(len(X)):
            if i < self.window:
                drawdowns.append(np.nan)
            else:
                past_window = close[i - (self.window-1):i]
                min_price = np.min(past_window)
                current_price = close[i-self.window]
                drawdown = (current_price - min_price) / current_price
                drawdowns.append(drawdown)

        col = f'Max_Drawdown_{self.window}d'
        X[col] = drawdowns  
        # X[f'{col}_shift1'] = X[col].shift(1)
        X[f'{col}_shift5'] = X[col].shift(5)
        X[f'{col}_shift10'] = X[col].shift(10)
        return X