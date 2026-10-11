import pandas as pd


def transform(dataframe: pd.DataFrame):
    """
    Clean data by dropping unneeded coloumns, renaming coloumns and parsing dates

    Args:
        dataframe (pd.DataFame): pandas DataFrame

    Returns:
        df (pd.DataFrame)
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

    return df

    

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
        "hire_date",
        "order_datetime"
    ]

    # Restructure dates to consiste format.
    for coloumn in date_columns:
        if coloumn in df.columns:
            df[coloumn] = pd.to_datetime(df[coloumn])

    return df