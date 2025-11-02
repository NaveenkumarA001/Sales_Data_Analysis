-- ===================================================
-- Retail Sales Database Setup Script
-- File: backend/database/retail_db.sql
-- ===================================================

-- 1️⃣ Drop old database if exists
DROP DATABASE IF EXISTS retail_db;

-- 2️⃣ Create a fresh database
CREATE DATABASE retail_db;

-- 3️⃣ Select the database
USE retail_db;

-- 4️⃣ Drop existing table if any
DROP TABLE IF EXISTS sales_data;

-- 5️⃣ Create the sales_data table
CREATE TABLE sales_data (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description TEXT,
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(10,2),
    CustomerID VARCHAR(20),
    Country VARCHAR(100)
);

-- ===================================================
-- 6️⃣ Load cleaned CSV data into MySQL table
-- IMPORTANT:
--    - Place your CSV file at:
--      C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\retail_data_clean.csv
--    - Ensure it uses Latin1 encoding (not UTF-8)
-- ===================================================

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/retail_data.csv'
INTO TABLE sales_data
CHARACTER SET latin1
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@InvoiceNo, @StockCode, @Description, @Quantity, @InvoiceDate, @UnitPrice, @CustomerID, @Country)
SET
    InvoiceNo   = @InvoiceNo,
    StockCode   = @StockCode,
    Description = @Description,
    Quantity    = @Quantity,
    InvoiceDate = STR_TO_DATE(@InvoiceDate, '%m/%d/%Y %H:%i'),
    UnitPrice   = @UnitPrice,
    CustomerID  = @CustomerID,
    Country     = @Country;

-- ===================================================
-- 7️⃣ Verify table structure and record count
-- ===================================================
SELECT COUNT(*) AS Total_Records FROM sales_data;
SELECT MIN(InvoiceDate) AS Start_Date, MAX(InvoiceDate) AS End_Date FROM sales_data;

-- ===================================================
-- ✅ END OF SCRIPT
-- ===================================================
