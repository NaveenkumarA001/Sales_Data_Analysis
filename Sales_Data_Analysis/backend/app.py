from flask import Flask, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# ✅ Paths
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/retail_data.csv')
REPORT_FILE = os.path.join(os.path.dirname(__file__), '../reports/summary_report.xlsx')


# ✅ Load & clean data
def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            print("❌ CSV not found.")
            return pd.DataFrame()

        df = pd.read_csv(DATA_FILE, encoding="ISO-8859-1")
        df = df.dropna(subset=["CustomerID", "Description"])
        df = df[df["Quantity"] > 0]
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
        df["UnitPrice"] = df["UnitPrice"].fillna(0)
        df["TotalSales"] = df["Quantity"] * df["UnitPrice"]
        df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

        print(f"✅ Loaded and cleaned {len(df)} rows.")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame()


# ✅ Perform summary calculations
def perform_analysis(df):
    return {
        "total_sales": round(df["TotalSales"].sum(), 2),
        "total_orders": int(df["InvoiceNo"].nunique()),
        "total_customers": int(df["CustomerID"].nunique())
    }


# ✅ Prepare chart data
def prepare_chart_data(df):
    country_sales = (
        df.groupby("Country")["TotalSales"]
        .sum()
        .reset_index()
        .sort_values(by="TotalSales", ascending=False)
        .head(5)
    )
    monthly_sales = (
        df.groupby("YearMonth")["TotalSales"]
        .sum()
        .reset_index()
        .sort_values(by="YearMonth")
    )
    return {
        "countries": {
            "labels": country_sales["Country"].tolist(),
            "values": [round(x, 2) for x in country_sales["TotalSales"]]
        },
        "months": {
            "labels": monthly_sales["YearMonth"].tolist(),
            "values": [round(x, 2) for x in monthly_sales["TotalSales"]]
        }
    }


# ✅ Save Excel Report Automatically
def save_to_excel(df):
    try:
        country_sales = (
            df.groupby("Country")["TotalSales"]
            .sum()
            .reset_index()
            .sort_values(by="TotalSales", ascending=False)
        )
        monthly_sales = (
            df.groupby("YearMonth")["TotalSales"]
            .sum()
            .reset_index()
            .sort_values(by="YearMonth")
        )
        top_items = (
            df.groupby("Description")["TotalSales"]
            .sum()
            .reset_index()
            .sort_values(by="TotalSales", ascending=False)
            .head(10)
        )

        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with pd.ExcelWriter(REPORT_FILE) as writer:
            country_sales.to_excel(writer, sheet_name="Country Sales", index=False)
            monthly_sales.to_excel(writer, sheet_name="Monthly Sales", index=False)
            top_items.to_excel(writer, sheet_name="Top Products", index=False)
        print(f"💾 Auto-saved Excel report to {REPORT_FILE}")
    except Exception as e:
        print(f"❌ Failed to save Excel: {e}")


# ✅ Routes
@app.route("/")
def home():
    return "<h2>Retail Data Analysis Backend</h2><p>Endpoints: /summary, /charts-data, /download-report</p>"


@app.route("/summary", methods=["GET"])
def summary():
    df = load_data()
    if df.empty:
        return jsonify({"error": "No data available"})
    result = perform_analysis(df)
    save_to_excel(df)  # <--- Auto-generate report
    return jsonify(result)


@app.route("/charts-data", methods=["GET"])
def charts_data():
    df = load_data()
    if df.empty:
        return jsonify({"error": "No data available"})
    result = prepare_chart_data(df)
    save_to_excel(df)  # <--- Auto-generate report
    return jsonify(result)


@app.route("/clean-data", methods=["GET"])
def clean_data():
    df = load_data()
    return jsonify(df.to_dict(orient="records"))


@app.route("/download-report", methods=["GET"])
def download_report():
    if not os.path.exists(REPORT_FILE):
        return jsonify({"error": "Report not found"}), 404
    return send_file(REPORT_FILE, as_attachment=True)


# ✅ Run app
if __name__ == "__main__":
    app.run(debug=True)
