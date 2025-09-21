def get_last_model(ticker,days):
    import sys
    try:
        import joblib
        import os
        from datetime import datetime

        models_dir = "/workspaces/Proyecto-Lab-2/Models/"
        models = os.listdir(models_dir)
        models = [m for m in models if m.split("_")[2] == ticker]
        models = [m for m in models if m.split("_")[1] == str(days)]

        def to_time(date):
            return datetime.strptime(date,"%Y-%m-%d %H:%M:%S")

        max_date = "0001-01-01 00:00:00"
        for m in models:
            time = m.split("_")[-1].replace(".joblib","")
            date = m.split("_")[-2]
            date_time = date + " " + time
            if to_time(date_time) > to_time(max_date):
                max_date = date_time
                best_model = m

        if best_model:
            return joblib.load(os.path.join(models_dir, best_model))
        
    except Exception as e:
        sys.exit(e)
        
print(get_last_model("^GSPC",5))
