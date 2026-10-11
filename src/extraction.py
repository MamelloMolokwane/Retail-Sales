import pandas as pd

def extract(filename: str, delimiter: str=",") -> pd.DataFrame:
    """
    Extracts data from file and returns the data into a structured pandas DataFrame

    Args:
        filename (str): CSV filename

    Return:
        pandas.DataFrame
    """

    try:
        df = pd.read_csv(filename, sep=delimiter)
        return df
    except FileNotFoundError:
        print(f"File {filename} not found")
        return None
