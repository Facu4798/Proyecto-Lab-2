select *,
    (open-close) as retorno,
    abs((open-close)/open) as variacion
from stock_data
inner join (
    select case 
               when count(*) over (order by date rows between current row and 10 following) < 10 
               then 0 
               else min(Close) over (order by date rows between current row and 10 following) 
           end as target,
           date
    from stock_data)
    on stock_data.date = stock_data.date
inner join macro_data on 
    month(stock_data.date) = month(macro_data.date) and
    year(stock_data.date) = year(macro_data.date)

