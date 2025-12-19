import sys
import pandas as pd
import duckdb
from datetime import datetime

# --- QMT IMPORT ---
try:
    from xtquant import xtdata
except ImportError:
    print("Error: Could not find xtquant.")
    sys.exit(1)

# --- CONFIGURATION ---
DB_PATH = 'market_data.duckdb'
BATCH_SIZE = 50 

def get_stock_list_from_db():
    """Fetches the list of active stocks from DuckDB."""
    con = duckdb.connect(DB_PATH)
    try:
        # Get all stocks where is_active is TRUE
        result = con.execute("SELECT stock_code FROM stock_universe WHERE is_active = TRUE").fetchall()
        # Result is a list of tuples [('000001.SZ',), ('600519.SH',)]
        # We need to flatten it to a simple list ['000001.SZ', '600519.SH']
        stock_list = [row[0] for row in result]
        return stock_list
    except Exception as e:
        print(f"Error fetching stock list: {e}")
        return []
    finally:
        con.close()

def save_batch_to_duckdb(df, table_name, db_path):
    # Same function as before...
    if df.empty: return
    con = duckdb.connect(db_path)
    con.register('df_temp', df)
    con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df_temp WHERE 1=0")
    
    # Deduplication Logic
    con.execute(f"""
        DELETE FROM {table_name} 
        WHERE (date, stock_code) IN (SELECT date, stock_code FROM df_temp)
    """)
    
    con.execute(f"INSERT INTO {table_name} SELECT * FROM df_temp")
    con.close()
    print(f"  > Saved {len(df)} rows.")

def run_batch_extraction():
    # 1. GET LIST FROM DB INSTEAD OF CSV
    stock_list = get_stock_list_from_db()
    
    if not stock_list:
        print("Stock universe is empty! Use 'manage_stocks.py' to add stocks.")
        return

    print(f"Loaded {len(stock_list)} active stocks from DuckDB.")
    total_stocks = len(stock_list)
    
    # 2. Process in Batches (Same as before)
    for i in range(0, total_stocks, BATCH_SIZE):
        batch_stocks = stock_list[i : i + BATCH_SIZE]
        print(f"\n--- Processing Batch {i//BATCH_SIZE + 1} ---")
        
        # Download
        for code in batch_stocks:
            xtdata.download_history_data(code, period='1d', start_time='20240101', end_time='20240130')
        
        # Read
        data_dict = xtdata.get_market_data(
            field_list=[], stock_list=batch_stocks, period='1d', 
            start_time='20240101', end_time='20240130', count=-1, 
            dividend_type='none', fill_data=True
        )
        
        # Transform
        all_dfs = []
        for code, df in data_dict.items():
            if not df.empty:
                df = df.reset_index()
                df.rename(columns={'index': 'date'}, inplace=True)
                df['stock_code'] = code 
                all_dfs.append(df)
        
        # Save
        if all_dfs:
            batch_df = pd.concat(all_dfs, ignore_index=True)
            save_batch_to_duckdb(batch_df, 'daily_kline', DB_PATH)

if __name__ == "__main__":
    run_batch_extraction()