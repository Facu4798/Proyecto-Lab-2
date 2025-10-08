with stock_curated as(
    select * from stock_data
    where Date <= CURRENT_DATE()
    and Date is not null
    and Ticker is not null
),
macro_curated as(
    select * from macro_data
    where Date <= CURRENT_DATE()
    and Date is not null
),