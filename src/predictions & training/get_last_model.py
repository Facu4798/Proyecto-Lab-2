def get_last_model(ticker,days):
    import sys
    try:
        import joblib
        import os
        from datetime import datetime

        models_dir = "/workspaces/Proyecto-Lab-2/Models/"
        models = [os.listdir(models_dir)]
        models = [m for m in models if m.split("_")[2] == ticker]
        models = [m for m in models if m.split("_")[1] == days]

        max_date = "0000-00-00"
        for m in models:
            date = m.split("_")[-1].replace(".joblib","")
            if datetime.strptime(date, "%Y-%m-%d") > datetime.strptime(max_date, "%Y-%m-%d"):
                max_date = date
                best_model = m

        if best_model:
            return joblib.load(os.path.join(models_dir, best_model))
        
    except Exception as e:
        sys.exit(e)
        
