import duckdb

DB_PATH = 'market_data.duckdb'

def add_stock(stock_code):
    con = duckdb.connect(DB_PATH)
    try:
        con.execute(f"""
            INSERT OR IGNORE INTO stock_universe (stock_code, added_date, is_active)
            VALUES ('{stock_code}', CURRENT_DATE, TRUE)
        """)
        print(f"Added {stock_code}")
    finally:
        con.close()

def remove_stock(stock_code):
    con = duckdb.connect(DB_PATH)
    try:
        # We don't delete, we just set inactive (safer)
        con.execute(f"UPDATE stock_universe SET is_active = FALSE WHERE stock_code = '{stock_code}'")
        print(f"Deactivated {stock_code}")
    finally:
        con.close()

def list_stocks():
    con = duckdb.connect(DB_PATH)
    res = con.execute("SELECT stock_code, is_active FROM stock_universe").df()
    print(res)
    con.close()

# Example Usage:
if __name__ == "__main__":
    # Choose what to do:
    # add_stock('002594.SZ')
    list_stocks()