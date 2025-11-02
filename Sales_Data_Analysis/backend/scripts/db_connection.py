# ===================================================
# File: backend/scripts/db_connection.py
# Description: Connects Flask backend to MySQL (retail_db)
# ===================================================

import mysql.connector
from mysql.connector import Error
import pandas as pd

# ---------------------------------------------------
# 1️⃣ MySQL Connection Configuration
# ---------------------------------------------------
def create_connection():
    """Create and return a database connection."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # Change if you use another MySQL username
            password="naveen@123",      # Enter your MySQL password here
            database="retail_db"
        )
        if connection.is_connected():
            print("✅ Connected to MySQL database: retail_db")
            return connection
    except Error as e:
        print("❌ Error while connecting to MySQL:", e)
        return None


# ---------------------------------------------------
# 2️⃣ Fetch all data from sales_data table
# ---------------------------------------------------
def fetch_all_data():
    """Fetch entire sales_data table as a DataFrame."""
    connection = create_connection()
    if connection:
        try:
            query = "SELECT * FROM sales_data;"
            df = pd.read_sql(query, connection)
            df['Country'] = df['Country'].str.replace('\r', '', regex=True)
            df['Description'] = df['Description'].str.replace('\r', '', regex=True)
            print(f"✅ Successfully loaded {len(df)} rows from sales_data table.")
            return df
        except Error as e:
            print("❌ Error while reading data:", e)
        finally:
            connection.close()
            print("🔒 MySQL connection closed.")


# ---------------------------------------------------
# 3️⃣ Fetch country-wise summary
# ---------------------------------------------------
def fetch_country_summary():
    """Fetch total orders by Country."""
    connection = create_connection()
    if connection:
        try:
            query = """
            SELECT Country, COUNT(*) AS Total_Orders
            FROM sales_data
            GROUP BY Country
            ORDER BY Total_Orders DESC;
            """
            df = pd.read_sql(query, connection)
            df['Country'] = df['Country'].str.replace('\r', '', regex=True)
            print("✅ Country summary fetched successfully.")
            return df
        except Error as e:
            print("❌ Error while reading data:", e)
        finally:
            connection.close()


# ---------------------------------------------------
# 4️⃣ Flask testing or direct execution
# ---------------------------------------------------
if __name__ == "__main__":
    # Example 1: Load entire dataset
    df = fetch_all_data()
    print(df.head())

    # Example 2: Get country summary
    summary_df = fetch_country_summary()
    print(summary_df.head())
