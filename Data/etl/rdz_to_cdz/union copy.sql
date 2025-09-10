WITH stock AS (
    SELECT Date, Ticker, Open, Close, High, Low, Volume
    FROM stock_data
    WHERE Date >= date_placeholder AND Ticker = ticker_placeholder
),
targets AS (
    SELECT Date,
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
    FROM stock_data where Date >= date_placeholder and Ticker = ticker_placeholder
),
cpiaucsl AS (
    SELECT Date, Value AS CPI
    FROM macro_data
    WHERE Series='CPIAUCSL' and Value IS NOT NULL and Date >= date_placeholder
),unrate AS (
    SELECT Date, Value AS Unemployment
    FROM macro_data
    WHERE Series='UNRATE' and Value IS NOT NULL and Date >= date_placeholder
),indpro AS (
    SELECT Date, Value AS Industrial_production
    FROM macro_data
    WHERE Series='INDPRO' and Value IS NOT NULL and Date >= date_placeholder
),fedfunds AS (
    SELECT Date, Value AS Fed_funds_rate
    FROM macro_data
    WHERE Series='FEDFUNDS' and Value IS NOT NULL and Date >= date_placeholder
),dgs10 AS (
    SELECT Date, Value AS Ten_year_treasury
    FROM macro_data
    WHERE Series='DGS10' and Value IS NOT NULL and Date >= date_placeholder
),pce AS (
    SELECT Date, Value AS PCE
    FROM macro_data
    WHERE Series='PCE' and Value IS NOT NULL and Date >= date_placeholder
),dff AS (
    SELECT Date, Value AS DFF
    FROM macro_data
    WHERE Series='DFF' and Value IS NOT NULL and Date >= date_placeholder
)
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
    targets.MinCloseOver10Days,
    targets.MinCloseOver5Days,
    targets.MinCloseOver30Days
FROM stock AS src
LEFT JOIN targets ON targets.Date = src.Date
LEFT JOIN cpiaucsl ON cpiaucsl.Date = src.Date
LEFT JOIN unrate ON unrate.Date = src.Date
LEFT JOIN indpro ON indpro.Date = src.Date
LEFT JOIN fedfunds ON fedfunds.Date = src.Date
LEFT JOIN dgs10 ON dgs10.Date = src.Date
LEFT JOIN pce ON pce.Date = src.Date
LEFT JOIN dff ON dff.Date = src.Date;

    
