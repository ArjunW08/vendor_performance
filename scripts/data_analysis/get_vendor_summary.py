import os
import sqlite3
import pandas as pd
import logging
from scripts.data_analysis.ingestion_db import inject_db

# Create logs directory if it doesn't exist
os.makedirs("../logs", exist_ok=True)

logging.basicConfig(
    filename="../logs/vendor_sales_summary.log",
    level=logging.DEBUG,
    force=True,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode="a",
)

def create_vendor_sales_summary(conn):
    '''This function creates a summary table for vendor sales performance.'''
    query = '''with FreightSummary as (
            select
            VendorNumber,
            sum(Freight) as FreightCost
            from vendor_invoice
            group by VendorNumber
        ),
            
        PurchaseSummary as (
            select
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.PurchasePrice,
            pp.Volume,
            sum(p.Quantity) as TotalPurchaseQuantity,
            sum(p.Dollars) as TotalPurchaseDollars,
            pp.Price as ActualPrice,
            p.Description
            from purchases p
            join purchase_prices pp
            on p.Brand = pp.Brand
            where p.PurchasePrice > 0
            group by p.VendorNumber, p.VendorName, p.Brand, p.PurchasePrice, pp.Volume, pp.Price, p.Description
        ),
            
        SalesSummary as (
            select 
                VendorNo,
                Brand,
                sum(SalesQuantity) as TotalSalesQuantity,
                sum(SalesDollars) as TotalSalesDollars,
                sum(SalesPrice) as TotalSalesPrice,
                sum(ExciseTax) as TotalExciseTax
            from sales
            group by VendorNo, Brand
        )

        select 
            ps.VendorNumber,
            ps.Brand,
            ps.VendorName,
            ps.PurchasePrice,
            ps.Description,
            ps.ActualPrice,
            ps.Volume,
            ps.TotalPurchaseQuantity,
            ps.TotalPurchaseDollars,
            ss.TotalSalesQuantity,
            ss.TotalSalesDollars,
            ss.TotalSalesPrice,
            ss.TotalExciseTax,
            fs.FreightCost
            from PurchaseSummary ps
            left join SalesSummary ss
            on ps.VendorNumber = ss.VendorNo
            and ps.Brand = ss.Brand
            left join FreightSummary fs
            on ps.VendorNumber = fs.VendorNumber
            order by ps.TotalPurchaseDollars desc
    '''
    vendor_sales_summary = pd.read_sql_query(query, conn)
    
    logging.info('Vendor sales summary created successfully')
    
    return vendor_sales_summary

def clean_data(df):
    '''This Function will clean te data'''
    # changing datatype to float
    df['Volume'] = df['Volume'].astype('float')

    # filling missing values with 0
    df.fillna(0,inplace=True)

    # removing spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # creating new columns for better analysis
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = df['GrossProfit'] / df['TotalSalesDollars'] * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

    return df

if __name__ == '__main__':
    # creating database connection
    conn = sqlite3.connect('inventory.db')

    logging.info("Creating Vendor Summary Table......")
    summary_df = create_vendor_sales_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning Data.....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting data......')
    inject_db(clean_df, 'vendor_sales_summary', conn)
    logging.info('Data ingested successfully')