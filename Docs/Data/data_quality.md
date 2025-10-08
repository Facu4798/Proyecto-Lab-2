# Data quality rules


## stock_data table
|Column|Rule|
|------|----|
|Date|is not null|
|Date|<=CURRENT_DATE()|
|Ticker|is not null|
|Open|>=0|
|Close|>=0|
|High|>=0|
|Low|>=0|
|Volume|>=0|

## macro_data table

|Column|Rule|
|------|----|
|Date|<=CURRENT_DATE()|
|Date|is not null|
|Series|is not null|