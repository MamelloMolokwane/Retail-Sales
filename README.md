# RYStore Retail Data ETL Pipeline

An end-to-end Python ETL pipeline that ingests raw retail CSV files, cleans and validates relational integrity using Pandas, loads them into a normalized SQLite database, and provides analytical SQL queries.

Designed for Week 1 Data Engineering practices focusing on Python, Pandas, data quality management, relational modeling, and SQL validation.

---

## Architecture Overview

```text
┌────────────────┐      ┌─────────────────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   Raw CSVs     │ ───► │ Extract, Clean & Validate   │ ───► │  SQLite Database │ ───► │   SQL Analytics  │
│ (customer, etc)│      │          (Pandas)           │      │   (rystore.db)   │      │ (Business KPIs)  │
└────────────────┘      └─────────────────────────────┘      └──────────────────┘      └──────────────────┘
```

The pipeline follows three core stages:
1. **Extract**: Reads the raw CSV sources and profiles schemas, data types, and initial record counts.
2. **Transform & Validate**: Normalizes text, enforces strict numeric and date formats, handles nulls/duplicates, and validates foreign key consistency across tables.
3. **Load**: Creates normalized relational tables with enforced primary and foreign key constraints in SQLite, persisting clean records idempotently.

---

## Datasets

The raw data is stored in `data/raw/` across five distinct files:

| File | Description | Core Responsibility |
| :--- | :--- | :--- |
| `customer.csv` | Customer demographic & contact details | Primary customer entity table |
| `products.csv` | Product listings, categories, and prices | Product catalog; references suppliers |
| `orders.csv` | Transaction headers, order dates, links | Core transactional table; references customers & stores |
| `stores.csv` | Store identifiers and geographical locations | Store directory |
| `suppliers.csv` | Supplier identifiers and vendor details | Supplier directory |

---

## Project Structure

```text
rystore-etl-pipeline/
├── data/
│   ├── raw/
│   │   ├── customer.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   ├── stores.csv
│   │   └── suppliers.csv
│   └── processed/
├── database/
│   └── retail_store.db
├── src/
│   ├── __init__.py
│   ├── extract.py         # CSV reading and initial schema validation
│   ├── transform.py       # Data cleansing, typing, and referential checks
│   ├── load.py            # SQLite schema creation and table insertion
│   └── pipeline.py        # Pipeline orchestrator
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites
* Python 3.9+
* Built-in `sqlite3` driver

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MamelloMolokwane/Retail-Sales
   cd Retail-Sales
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Pipeline

Execute the full extraction, transformation, and database load via the main runner:

```bash
python src/pipeline.py
```

### Running Tests
To run unit and integration tests across data transforms and constraints:

```bash
pytest
```

---

## Data Cleaning & Transformation Rules

All raw data remains immutable in `data/raw/`. Cleaned representations are output to `data/processed/` before database loading.

* **Missing Values**: Profiled per column. Essential business identifiers with null values are dropped; optional categorical fields are imputed or set to `NULL`.
* **Duplicates**: Exact duplicate rows and conflicting primary keys are purged.
* **Text Standardization**: String fields are trimmed of leading/trailing whitespace and normalized.
* **Numeric Casting**: Currency, prices, and quantities are parsed to explicit `FLOAT` and `INTEGER` types.
* **Date Parsing**: Date strings are parsed and formatted into standard ISO-8601 (`YYYY-MM-DD HH:MM:SS`).
* **Referential Integrity**: Child records referencing non-existent parent keys (e.g., an order with an invalid `customer_id` or `store_id`) are flagged and isolated to prevent orphaned database records.

---

## Database Schema & Constraints

The SQLite database enforces foreign key constraints at connection startup:
```sql
PRAGMA foreign_keys = ON;
```

### Entity Relationship Model

```text
  [suppliers]
       │
       ▼ (1:N)
   [products]

   [customers]         [stores]
       │                  │
       └────► [orders] ◄──┘
               (N:1)
```

Tables are loaded in hierarchical order to respect relational constraints:
1. Parent tables: `customers`, `stores`, `suppliers`
2. Dependent tables: `products`, `orders`

---

## Analytical SQL Queries

Once the database is generated at `database/rystore.db`, you can run analytical queries using SQLite CLI or your favorite database client.

### Top Stores by Order Volume
```sql
SELECT 
    s.store_id,
    s.store_name,
    COUNT(o.order_id) AS total_orders
FROM stores s
JOIN orders o ON s.store_id = o.store_id
GROUP BY s.store_id, s.store_name
ORDER BY total_orders DESC;
```

### Monthly Order Counts
```sql
SELECT 
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY order_month
ORDER BY order_month ASC;
```

### Top 5 Customers by Order Frequency
```sql
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY order_count DESC
LIMIT 5;
```

### Product Catalog Breakdown by Supplier
```sql
SELECT 
    sp.supplier_id,
    sp.supplier_name,
    COUNT(p.product_id) AS products_supplied
FROM suppliers sp
JOIN products p ON sp.supplier_id = p.supplier_id
GROUP BY sp.supplier_id, sp.supplier_name
ORDER BY products_supplied DESC;
```

---

## Definition of Done (DoD)

- [ ] **Data Ingestion**: Reads all 5 CSV files with clear error handling for missing files.
- [ ] **Repeatable Cleaning**: Transforms execute deterministically with identical inputs.
- [ ] **Quality Metrics**: Logs record counts: ingested, transformed, flagged, and rejected.
- [ ] **Referential Integrity**: Zero orphaned records loaded into relational tables.
- [ ] **SQLite Persistence**: Schema loads successfully with primary and foreign keys active.
- [ ] **Idempotent Runs**: Re-executing `pipeline.py` maintains valid state without duplicate records.
- [ ] **Verification**: Core business and data quality queries execute cleanly.