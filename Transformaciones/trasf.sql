select 
        open,
        close,
        low,
        high,
        volume,
        (open-close) as retorno,

from stock_data