SELECT      
            src.Date,
            src.Ticker,
            src.Open,
            src.Close,
            src.High,
            src.Low,
            src.Volume,
            cpiaucsl.Value as CPI,
            unrate.Value as Unemployment,
            indpro.Value as Industrial_production,
            fedfunds.Value as Fed_funds_rate,
            dgs10.Value as 10_year_treasury,
            pce.Value as PCE,
            dff.Value as DFF,
            (MinCloseOver10Days-src.close)/src.Close as Target10,
            (MinCloseOver5Days-src.Close)/src.Close as Target5,
            (MinCloseOver30Days-src.Close)/src.Close as Target30
    FROM stock_data AS src 
    INNER JOIN (
        SELECT  Date,
                CASE
                    WHEN COUNT(*) OVER (ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND 10 FOLLOWING) < 10
                    THEN MIN(Close) OVER (ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND UNBOUNDED FOLLOWING)
                    ELSE MIN(Close) OVER (ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND 10 FOLLOWING)
                END AS MinCloseOver10Days,
                CASE
                    WHEN COUNT(*) OVER(ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND 5 FOLLOWING) < 5
                    THEN MIN(Close) OVER (ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND UNBOUNDED FOLLOWING)
                    ELSE MIN(Close) OVER (ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND 5 FOLLOWING)
                END AS MinCloseOver5Days,
                CASE
                    WHEN COUNT(*) OVER(ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND 30 FOLLOWING) < 30
                    THEN MIN(Close) OVER (ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND UNBOUNDED FOLLOWING)
                    ELSE MIN(Close) OVER (ORDER BY date ASC ROWS BETWEEN 1 FOLLOWING AND 30 FOLLOWING)
                END AS MinCloseOver30Days
        FROM stock_data where Date >= date_placeholder  
        ) AS tar ON tar.Date = src.Date
    LEFT JOIN (
        SELECT  Date,
                Value
        FROM macro_data
        WHERE Series='CPIAUCSL' and Value IS NOT NULL and Date >= date_placeholder
        ) AS cpiaucsl ON cpiaucsl.Date = src.Date
    LEFT JOIN (
        SELECT  Date,
                Value
        FROM macro_data
        WHERE Series='UNRATE' and Value IS NOT NULL and Date >= date_placeholder
        ) AS unrate ON unrate.Date = src.Date
    LEFT JOIN (
        SELECT  Date,
                Value
        FROM macro_data
        WHERE Series='INDPRO' and Value IS NOT NULL and Date >= date_placeholder
        ) AS indpro ON indpro.Date = src.Date
    LEFT JOIN (
        SELECT  Date,
                Value
        FROM macro_data
        WHERE Series='FEDFUNDS' and Value IS NOT NULL and Date >= date_placeholder
        ) AS fedfunds ON fedfunds.Date = src.Date
    LEFT JOIN (
        SELECT  Date,
                Value
        FROM macro_data
        WHERE Series='DGS10' and Value IS NOT NULL and Date >= date_placeholder
        ) AS dgs10 ON dgs10.Date = src.Date
    LEFT JOIN (
        SELECT  Date,
                Value
        FROM macro_data
        WHERE Series='PCE' and Value IS NOT NULL and Date >= date_placeholder
        ) AS pce ON pce.Date = src.Date
    LEFT JOIN (
        SELECT  Date,
                Value
        FROM macro_data
        WHERE Series='DFF' and Value IS NOT NULL and Date >= date_placeholder
        ) AS dff ON dff.Date = src.Date
    ;