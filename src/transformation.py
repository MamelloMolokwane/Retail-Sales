import pandas as pd

# Ideas on how to clean the data. 
#  * There are multiple coloumns from multiple CSVs that you want to drop. 
#       - An idea is to store the coloumn names you want to drop into a list and if it exist in the DataFrame drop it from the DataFrame.
#  * Rename "postcode_area" to "postcode" for coloumn name consistency.
#  * figure out how to handle dates and datatimes.
#  * Set the numbers to explicit 'FLOAT' if they're currency and 'INTEGER' if it's just a number - This is automatically done by pd.read_csv

def transform(dataframe: pd.DataFrame):
    """
    Clean data by dropping unneeded coloumns, renaming coloumns and parsing dates then saving the cleaned data to data/processed/

    Args:
        dataframe (pd.DataFame): pandas DataFrame

    Returns:
        Returns Nothing
    """

    # Drop unneeded coloumns from the DataFrame
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
    df_with_dropped_coloumns = dataframe.drop(columns=coloumns, errors="ignore")

    # Rename "postcode_area" to "postcode" for coloumn name consistency
    if "postcode_area" in df_with_dropped_coloumns.columns:
        df_with_dropped_coloumns.rename(columns={"postcode_area": "postcode"}, inplace=True)

    # Parse dates to DateTime object and maintain consistency
    df = date_parsing(df_with_dropped_coloumns)

    # Create the output filename from the first column's name which should be the id column for the table.
    # For example, "customer_id" becomes "customers.csv".
    csv_name = df.columns[0].split("_")[0]
    df.to_csv(f"./data/processed/{csv_name}s.csv", index=False)

    

def date_parsing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse dates to DateTime object and keep consistent formatting

    Args:
        df (pd.DataFrame): pandas DataFrame

    Returns:
        Returns pandas DataFrame
    """

    date_columns = [
        "opening_date",
        "signup_date",
        "hire_date"
    ]

    # Restructure dates to consiste format.
    for coloumn in date_columns:
        if coloumn in df.columns:
            df[coloumn] = pd.to_datetime(df[coloumn])

    # Edit "order_datetime" separtely as it includes the time
    if "order_datetime" in df.columns:
        df["order_datetime"] = pd.to_datetime(df["order_datetime"])

    return df