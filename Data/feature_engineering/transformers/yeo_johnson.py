

class YeoJohnsonTransformer:
    def __init__(self, columns):
        self.columns = columns
        self.transformers = {}

    def fit(self, x, y=None):
        from sklearn.preprocessing import PowerTransformer
        for col in self.columns:
            transformer = PowerTransformer(method='yeo-johnson', standardize=self.standardize)
            transformer.fit(x[col].values.reshape(-1, 1))
            self.transformers[col] = transformer
        return self

    def transform(self, x):
        
        x = x.copy()
        for col in self.columns:
            x[col] = self.transformers[col].transform(x[col].values.reshape(-1, 1))
        return x

    