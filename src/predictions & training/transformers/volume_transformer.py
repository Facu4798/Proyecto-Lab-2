class VolumeTransformer:
    def __init__(self,window):
        self.window = window

    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        x = x.copy()
        # media movil de volume
        x["mmv"] = x['Volume'].rolling(window=2).mean()
        x["Volume"] = (x["Volume"]- x["mmv"])/ x["mmv"]
        x = x.drop(columns=["mmv"])
        x["Volume"] = x["Volume"].fillna(0)
        #replace inf with 0
        import numpy as np
        x["Volume"] = x["Volume"].replace([np.inf, -np.inf], 0)

        return x