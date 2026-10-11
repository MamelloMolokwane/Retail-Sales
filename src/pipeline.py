from extraction import extract
import pandas as pd

customer = extract("./data/raw/customers.csv")
# print("file is running.")
print(customer.head(3))