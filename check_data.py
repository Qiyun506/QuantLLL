import duckdb

# Connect to the database
con = duckdb.connect('market_data.duckdb')

# Check which tables exist
print("--- Tables in Database ---")
print(con.execute("SHOW TABLES").df())

# Peek at the data
print("\n--- First 5 Rows of stock_universe ---")
try:
    print(con.execute("SELECT * FROM stock_universe LIMIT 5").df())
except:
    print("stock_universe table not found.")

print("\n--- First 5 Rows of daily_kline ---")
try:
    print(con.execute("SELECT * FROM daily_kline LIMIT 5").df())
except:
    print("daily_kline table not found.")