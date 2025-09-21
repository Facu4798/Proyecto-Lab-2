class arch_model:
    def __str__(self):
        return self.name
    
    def __init__(self,params = {},model_name="ARCH"):
        self.name = model_name
        for key in params:
            setattr(self,key,params[key])
    
    def fit(self, x,y):
        pass
        return self
    
    def get_params(self):
        params = {}
        return params
    
    def predict(self, x):
        preds = []
        return preds