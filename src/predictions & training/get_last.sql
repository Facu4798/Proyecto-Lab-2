SELECT  src.Date,
        src.Ticker,
        src.Open,
        src.Close,
        src.High,
        src.Low,
        src.Volume,
        (src.Open - src.Close) AS retorno,
        (src.Open - src.Close) / src.Open AS retorno_porcentaje,
        ABS(src.High - src.Low) AS amplitud,
        ABS(src.High - src.Low) / src.Open AS amplitud_porcentaje,
        CPI,
        Unemployment,
        Industrial_production,
        Fed_funds_rate,
        10_year_treasury,
        PCE,
        DFF,
        Target10,
        Target5,
        Target30
FROM curated as src
ORDER BY src.Date DESC
LIMIT 400;