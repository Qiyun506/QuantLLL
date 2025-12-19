import duckdb
import pandas as pd

DB_PATH = 'market_data.duckdb'
CSV_PATH = 'stock_list.csv'

def initialize_universe():
    con = duckdb.connect(DB_PATH)
    
    # 1. Create the 'stock_universe' table
    # We add 'is_active' so you can "pause" a stock without deleting it
    con.execute("""
        CREATE TABLE IF NOT EXISTS stock_universe (
            stock_code VARCHAR PRIMARY KEY,
            added_date DATE DEFAULT CURRENT_DATE,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    
    # 2. Read your current CSV
    try:
        # Assuming your CSV has a header 'code'. If not, use names=['code']
        df = pd.read_csv(CSV_PATH)

        df.rename(columns={'code': 'stock_code'}, inplace=True)
        # Rename column to match our SQL table
        
        # Add default values for the new columns
        df['is_active'] = True
        df['added_date'] = pd.Timestamp.now().date()
        
        df = df[['stock_code', 'added_date', 'is_active']]
        # 3. Insert into DuckDB (Ignore duplicates)
        con.register('df_temp', df)
        con.execute("""
            INSERT OR IGNORE INTO stock_universe (stock_code, added_date, is_active)
            SELECT stock_code, added_date, is_active FROM df_temp
        """)
        
        print(f"Successfully migrated {len(df)} stocks to DuckDB!")
        
    except Exception as e:
        print(f"Error reading CSV or inserting: {e}")
        
    con.close()

if __name__ == "__main__":
    initialize_universe()