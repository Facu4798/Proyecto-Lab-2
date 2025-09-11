def get_last_model(ticker,target):
    import os
    from datetime import datetime
    from datetime import strptime,strftime
    files = os.listdir("/workspaces/Proyecto-Lab-2/Models")
    for f in files:
        if f.split("modelo_")[1][0] != target:
            files.remove(f)
    max_date = "0000-00-00 00:00:00"
    for f in files:
        cur_date = f.split(f"modelo_{target}_{ticker}_")[1]
        if strptime(cur_date, "%Y-%m-%d %H:%M:%S") > strptime(max_date, "%Y-%m-%d %H:%M:%S"):
            max_date = cur_date
    max_date = strftime("%Y-%m-%d %H:%M:%S", strptime(max_date, "%Y-%m-%d %H:%M:%S"))
    return f"modelo_{target}_{ticker}_{max_date}.joblib"

