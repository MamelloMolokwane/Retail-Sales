from transformation import transform
from extraction import extract
from loading import load
import pandas as pd

def pipeline():
    """
    Runs the ETL pipeline for the RYStore dataset.

    Extracts raw data from the customers, employees, orders, products,
    stores, and suppliers CSV files. Transforms each dataset by cleaning
    and preparing the data, then loads the cleaned DataFrames into the
    processed data directory.

    Returns:
    None: The function saves the processed datasets through the
    load() function and does not return a value.

    """

    # Define file locations
    customers_raw = "./data/raw/customers.csv"
    employees_raw = "./data/raw/employees.csv"
    orders_raw = "./data/raw/orders.csv" 
    product_raw = "./data/raw/products.csv"
    stores_raw = "./data/raw/stores.csv"
    suppliers_raw = "./data/raw/suppliers.csv"

    # Extract all the data
    customers = extract(customers_raw)
    employees = extract(employees_raw)
    orders = extract(orders_raw)
    products = extract(product_raw)
    stores = extract(stores_raw)
    suppliers = extract(suppliers_raw)

    # Clean all the extracted data
    customers_df = transform(customers)
    employees_df = transform(employees)
    orders_df = transform(orders)
    products_df = transform(products)
    stores_df = transform(stores)
    suppliers_df = transform(suppliers)

    # Load the cleaned data
    load(customers_df, employees_df, orders_df, products_df, stores_df, suppliers_df)
    # load(employees_df)
    # load(orders_df)
    # load(products_df)
    # load(stores_df)
    # load(suppliers_df)

if __name__ == "__main__":
    pipeline()