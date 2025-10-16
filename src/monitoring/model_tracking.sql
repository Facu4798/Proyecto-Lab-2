WITH pred_f AS(select * from predicciones where Ticker = 'ticker_placeholder'),
        cur_f AS(select * from curated where Ticker = 'ticker_placeholder'),
        pre AS (
            SELECT c.date as curated_date, 
                p.date as prediction_date,
                c.Targett_placeholder as real_value,
                p.t_placeholderDays prediction,
                c.Ticker 
            FROM cur_f c 
            INNER JOIN pred_f p
            ON c.Date = DATE_ADD(p.Date, INTERVAL t_placeholder DAY)
        )
        SELECT MAX(pre.prediction_date) as Date, 
        AVG(ABS(pre.prediction-pre.real_value)) as MAE,
        'ticker_placeholder' AS Ticker, 
        't_placeholder' as Days
        FROM pre