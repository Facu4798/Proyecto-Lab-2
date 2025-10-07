class BLFImputer:

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        na_columns = X.columns[X.isna().any()]

        # Backfill para valores iniciales
        for col in na_columns:
            first_valid_index = X[col].first_valid_index()
            if first_valid_index is not None:
                X.loc[:first_valid_index, col] = X.loc[:first_valid_index, col].bfill()

        # Forward fill para valores finales
        for col in na_columns:
            last_valid_index = X[col].last_valid_index()
            if last_valid_index is not None:
                X.loc[last_valid_index:, col] = X.loc[last_valid_index:, col].ffill()

        # Interpolación lineal para el resto
        X.interpolate(method='linear', inplace=True)

        return X