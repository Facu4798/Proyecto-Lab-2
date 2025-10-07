class model_template:
    def __str__(self):
        return self.name
    
    def __init__(self,
                vol="Garch", 
                p=1, 
                q=1,
                o=0, 
                mean="Zero", 
                rescale=True, 
                exog_cols=None):
        
        self.name = vol
        self.vol = vol
        self.p = p
        self.q = q
        self.o = o
        self.mean = mean
        self.rescale = rescale
        self.exog_cols = exog_cols  # solo para REGARMA
        self.model = None
        self.res = None

    
    def fit(self, y, x=None):
        from arch import arch_model
        if self.exog_cols is not None and x is not None:
            self.model = arch_model(y,
                                    x=x,
                                    vol=self.vol,
                                    p=self.p, q=self.q, o=self.o,
                                    mean=self.mean,
                                    rescale=self.rescale)
        else:
            self.model = arch_model(y,
                                    vol=self.vol,
                                    p=self.p, q=self.q, o=self.o,
                                    mean=self.mean,
                                    rescale=self.rescale)
            
        self.res = self.model.fit(disp="off")
        return self
    
    
    def predict(self, steps=5, exog_future=None):
        import pandas as pd
        import numpy as np
        """Genera predicciones de volatilidad (sigma)."""
        if self.exog_cols is not None and exog_future is not None:
            # Caso REGARMA con múltiples exógenas
            if isinstance(exog_future, pd.DataFrame):
                if len(self.exog_cols) == 1: # una sola exógena
                    x_new = exog_future.values.reshape(1, -1)  
                else:
                    x_new = {col: exog_future[col].values for col in self.exog_cols}
            else:
                x_new = exog_future
            fc = self.res.forecast(horizon=steps, x=x_new, reindex=False)


            return np.sqrt(fc.variance.values[-1,:])
        
        
        else:
            # Caso sin exógenas
            fc = self.res.forecast(horizon=steps, reindex=False)
            return np.sqrt(fc.variance.values[-1,:])
    
    def get_params(self):
        params = {
            "p": self.p,
            "q": self.q,
            "o": self.o,
            "mean": self.mean,
            "rescale": self.rescale,
            "exog_cols": self.exog_cols
        }
        return params
