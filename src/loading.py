import pandas as pd
import sqlite3

# Remember to set the "..._id" from each DataFrame into a primary key. If saving to SQL. 
# IMPLEMENTATION INCOMPLETE SAVE TO SQLITE DATABASE

def load(customers_df: pd.DataFrame, employees_df: pd.DataFrame, orders_df: pd.DataFrame, products_df: pd.DataFrame, stores_df: pd.DataFrame, suppliers_df: pd.DataFrame):
    """
    Save the cleaned data to data/processed/

    Args:
        customers_df (pd.DataFrame): pandas DataFrame
        employees_df (pd.DataFrame): pandas DataFrame
        orders_df (pd.DataFrame): pandas DataFrame
        products_df (pd.DataFrame): pandas DataFrame
        stores_df (pd.DataFrame): pandas DataFrame
        suppliers_df (pd.DataFrame): pandas DataFrame

    Returns:
        Returns nothing
    """
    # Create the output filename from the first column's name which should be the id column for the table.
    # For example, "customer_id" becomes "customers.csv".
    datasets = {
        "customers": customers_df,
        "employees": employees_df,
        "orders": orders_df,
        "products": products_df,
        "stores": stores_df,
        "suppliers": suppliers_df
    }

    # Save each cleaned DataFrame as a CSV file.
    for name, df in datasets.items():
        df.to_csv(f"./data/processed/{name}.csv", index=False)

    # Now I need to save the data to a sqlite database
    # I might need to use actual SQL to create the table so that I can set Primary keys and Foreighn keys coloumns
    conn = sqlite3.connect("./data/database/retail_store.db")
    
    create_tables(conn, customers_df, employees_df, orders_df, products_df, stores_df, suppliers_df)
    conn.commit()

    

def create_tables(conn, customers_df, employees_df, orders_df, products_df, stores_df, suppliers_df):
    """
    Creates SQLite tables

    Args:
        cursor (Sqlite cursor)
        customers_df (pd.DataFrame): pandas DataFrame
        employees_df (pd.DataFrame): pandas DataFrame
        orders_df (pd.DataFrame): pandas DataFrame
        products_df (pd.DataFrame): pandas DataFrame
        stores_df (pd.DataFrame): pandas DataFrame
        suppliers_df (pd.DataFrame): pandas DataFrame

    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create customers table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                city TEXT NOT NULL,
                postcode TEXT NOT NULL,
                signup_date TEXT NOT NULL
            )
        """)
    customers_df.to_sql("customers", conn, if_exists="append", index=False)
    
    # Create stores table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                store_id TEXT PRIMARY KEY NOT NULL,
                store_name TEXT NOT NULL,
                city TEXT NOT NULL,
                region TEXT NOT NULL,
                postcode TEXT NOT NULL,
                store_format TEXT NOT NULL,
                opening_date TEXT NOT NULL,
                staff_count INTEGER NOT NULL
            )
        """)
    stores_df.to_sql("stores", conn, if_exists="append", index=False)
    
    # Create employees table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                store_id TEXT NOT NULL,
                role TEXT NOT NULL,
                hire_date TEXT NOT NULL,
                contract_type TEXT NOT NULL,
                annual_salary INTEGER NOT NULL,

                FOREIGN KEY (store_id) REFERENCES stores(store_id)
            )
        """)
    employees_df.to_sql("employees", conn, if_exists="append", index=False)

    # Create orders table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY NOT NULL,
                order_datetime TEXT NOT NULL,
                order_channel TEXT NOT NULL,
                order_status TEXT NOT NULL,
                subtotal REAL NOT NULL,
                discount_total REAL NOT NULL,
                vat_total REAL NOT NULL,
                delivery_fee REAL NOT NULL,
                total_amount REAL NOT NULL,

                store_id TEXT NOT NULL,
                customer_id TEXT,

                FOREIGN KEY (store_id) REFERENCES stores(store_id),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
    """)
    orders_df.to_sql("orders", conn, if_exists="append", index=False)

    # Create suppliers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id TEXT PRIMARY KEY NOT NULL,
            supplier_name TEXT NOT NULL,
            main_category TEXT NOT NULL,
            city TEXT NOT NULL,
            postcode TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    suppliers_df.to_sql("suppliers", conn, if_exists="append", index=False)

    # Create products table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            supplier_id TEXT NOT NULL,
            unit_cost REAL NOT NULL,
            unit_price REAL NOT NULL,
            vat_rate REAL NOT NULL,

            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
            )
    """)
    products_df.to_sql("products", conn, if_exists="append", index=False)

    print("Tables created")

