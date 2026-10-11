import pandas as pd

# Ideas on how to clean the data. 
#  * There are multiple coloumns from multiple CSVs that you want to drop. 
#       - An idea is to store the coloumn names you want to drop into a list and if it exist in the DataFrame drop it from the DataFrame.
#  * Rename "postcode_area" to "postcode" for coloumn name consistency.
#  * figure out how to handle dates and datatimes.
#  * Set the numbers to explicit 'FLOAT' if they're currency and 'INTEGER' if it's just a number

def transform(dataframe: pd.DataFrame) -> pd.DataFrame:
    coloumns = [
        "loyalty_tier",
        "customer_segment",
        "marketing_opt_in",
        "brand",
        "active",
        "reorder_level",
        "lead_time_days",
        "payment_method",

    ]
    ...