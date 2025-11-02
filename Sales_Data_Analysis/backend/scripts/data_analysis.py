import pandas as pd
import os

# ✅ File paths
DATA_FILE = os.path.join(os.path.dirname(__file__), '../../data/retail_data.csv')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '../../reports/summary_report.xlsx')

# ✅ Load and clean dataset
def load_and_clean_data():
    try:
        print(f"📁 Loading data from: {DATA_FILE}")
        df = pd.read_csv(DATA_FILE, encoding='ISO-8859-1')

        # Drop missing values
        df = df.dropna(subset=['CustomerID', 'Description'])
        df = df[df['Quantity'] > 0]

        # Convert date column
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

        # Fill missing prices
        df['UnitPrice'] = df['UnitPrice'].fillna(0)

        # Add computed columns
        df['TotalSales'] = df['Quantity'] * df['UnitPrice']
        df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)

        print(f"✅ Loaded and cleaned {len(df)} rows.")
        return df
    except Exception as e:
        print("❌ Error loading data:", e)
        return pd.DataFrame()


# ✅ Summary metrics function (from your code)
def perform_analysis(df):
    total_sales = (df['Quantity'] * df['UnitPrice']).sum()
    total_orders = df['InvoiceNo'].nunique()
    total_customers = df['CustomerID'].nunique()

    summary = {
        "total_sales": round(total_sales, 2),
        "total_orders": int(total_orders),
        "total_customers": int(total_customers)
    }

    print("\n📊 Quick Summary:")
    print(summary)
    return summary


# ✅ Analysis 1: Total Revenue by Country
def revenue_by_country(df):
    country_sales = df.groupby('Country')['TotalSales'].sum().reset_index()
    country_sales = country_sales.sort_values(by='TotalSales', ascending=False)
    print("\n🌍 Top 5 Countries by Revenue:")
    print(country_sales.head())
    return country_sales


# ✅ Analysis 2: Monthly Sales Trend
def monthly_sales_trend(df):
    monthly_sales = df.groupby('YearMonth')['TotalSales'].sum().reset_index()
    monthly_sales = monthly_sales.sort_values(by='YearMonth')
    print("\n📆 Monthly Sales Trend:")
    print(monthly_sales.head())
    return monthly_sales


# ✅ Analysis 3: Top Products by Sales
def top_products(df):
    top_items = df.groupby('Description')['TotalSales'].sum().reset_index()
    top_items = top_items.sort_values(by='TotalSales', ascending=False).head(10)
    print("\n🏆 Top 10 Products by Sales:")
    print(top_items)
    return top_items


# ✅ Save all summaries to Excel
def save_to_excel(country_sales, monthly_sales, top_items):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with pd.ExcelWriter(OUTPUT_FILE) as writer:
        country_sales.to_excel(writer, index=False, sheet_name='Country Sales')
        monthly_sales.to_excel(writer, index=False, sheet_name='Monthly Sales')
        top_items.to_excel(writer, index=False, sheet_name='Top Products')
    print(f"\n💾 Summary report saved to: {OUTPUT_FILE}")


# ✅ Run the full pipeline
if __name__ == "__main__":
    df = load_and_clean_data()

    if not df.empty:
        # Quick summary
        perform_analysis(df)

        # Detailed analyses
        country_sales = revenue_by_country(df)
        monthly_sales = monthly_sales_trend(df)
        top_items = top_products(df)

        # Save report
        save_to_excel(country_sales, monthly_sales, top_items)

        print("\n🎉 Analysis complete! Check 'reports/summary_report.xlsx' for results.")
