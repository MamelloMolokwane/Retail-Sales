import pandas as pd

# Remember to set the "..._id" from each DataFrame into a primary key.

def load(df: pd.DataFrame):
    """
    Save the cleaned data to data/processed/

    Args:
        df (pd.DataFrame): pandas DataFrame

    Returns:
        Returns nothing
    """
    # Create the output filename from the first column's name which should be the id column for the table.
    # For example, "customer_id" becomes "customers.csv".
    csv_name = df.columns[0].split("_")[0]
    df.to_csv(f"./data/processed/{csv_name}s.csv", index=False)