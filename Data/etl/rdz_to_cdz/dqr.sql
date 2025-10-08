with stock_curated as(
    select * from stock_data
    where Date <= CURRENT_DATE()
    and Date is not null
    and Ticker is not null
    and Open >= 0
    and Close >= 0
    and High >= 0
    and Low >= 0
    and Volume >= 0
),
macro_curated as(
    select * from macro_data
    where Date <= CURRENT_DATE()
    and Date is not null
    and Series is not null
),