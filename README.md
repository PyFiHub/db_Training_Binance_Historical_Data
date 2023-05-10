# db_Training_Binance_Historical_Data
SQL and Python Practice - Coin/Token Binance
<br />
<br />

## Summary

- [Useful SQL Commands for Data Analysis](#useful-sql-commands-for-data-analysis)
- [Useful SQL Commands for Technical Analysis](#useful-sql-commands-for-technical-analysis)
- [Python Samples - How to implement SQL in Python](#python-samples---how-to-implement-sql-in-python)

## SQL Playground: [Streamlit Cloud](https://pyfihub-streamlit-apps-streamlit-sql-db-uo2s89.streamlit.app)

<br />


### <a id="useful-sql-commands-for-data-analysis"></a>Useful SQL Commands for Data Analysis

**SELECT**:

The SELECT statement is used to query the data from the table. You can retrieve specific columns or all columns from the table.
Example: Retrieve all columns from the "pair_BTCUSDT" table.

```sql
SELECT * FROM pair_BTCUSDT;
```

<br />

**WHERE**:

The WHERE clause is used to filter records based on a specified condition.
Example: Retrieve records from the "pair_BTCUSDT" table where the closing price is greater than 50000.

```sql
SELECT * FROM pair_BTCUSDT WHERE close > 50000;
```

<br />

**ORDER BY**:

The ORDER BY clause is used to sort the records in ascending or descending order based on one or more columns.
Example: Sort records from the "pair_BTCUSDT" table by closing price in descending order.

```sql
SELECT * FROM pair_BTCUSDT ORDER BY close DESC;
```

<br />

**LIMIT**:

The LIMIT clause is used to constrain the number of records returned by the SELECT statement.
Example: Retrieve the top 10 records from the "pair_BTCUSDT" table with the highest closing prices.

```sql
SELECT * FROM pair_BTCUSDT ORDER BY close DESC LIMIT 10;
```

<br />

**COUNT**:

The COUNT function returns the number of records that match a specified condition.
Example: Count the number of records in the "pair_BTCUSDT" table where the closing price is greater than 50000.

```sql
SELECT COUNT(*) FROM pair_BTCUSDT WHERE close > 50000;
```

<br />

**AVG, MIN, MAX, SUM**:
    
These aggregate functions are used to compute the average (AVG), minimum (MIN), maximum (MAX), and sum (SUM) of a set of records.
Example: Calculate the average, minimum, and maximum closing prices, and the total volume for the "pair_BTCUSDT" table.

```sql
SELECT AVG(close) AS average_close, MIN(close) AS min_close, MAX(close) AS max_close, SUM(volume) AS total_volume
FROM pair_BTCUSDT;
```

<br />

**GROUP BY**:

The GROUP BY clause is used to group rows with the same values in specified columns into groups, like when using aggregate functions.
Example: Calculate the average closing price for each day in the "pair_BTCUSDT" table.

```sql
SELECT DATE(open_time) AS date, AVG(close) AS average_close
FROM pair_BTCUSDT
GROUP BY date;
```

<br />

**HAVING**:

The HAVING clause is used to filter the results of a GROUP BY query, based on a condition that applies to the aggregated data.
Example: Find the days where the average closing price was greater than 50000 in the "pair_BTCUSDT" table.

```sql
SELECT open_time, SUM(volume) as daily_volume
FROM pair_BTCUSDT
GROUP BY open_time
HAVING daily_volume > 10000;
```

<br />

**JOIN**:

JOIN: This operation is used to combine rows from two or more tables based on a related column between them. There are different types of JOINs, such as INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN.
Example: Retrieve data from two related tables (assuming you have another table called pair_ETHUSDT)

```sql
SELECT A.open_time, A.close AS BTC_close, B.close AS ETH_close
FROM pair_BTCUSDT AS A
INNER JOIN pair_ETHUSDT AS B ON A.open_time = B.open_time;
```

<br />

**CASE**:

CASE: This statement allows you to perform conditional logic in SQL queries. It is useful when you want to create new columns based on the values in the existing columns.
Example: Categorize the days based on the closing price

```sql
SELECT open_time, close,
       CASE
           WHEN close < 30000 THEN 'Low'
           WHEN close >= 30000 AND close < 60000 THEN 'Medium'
           ELSE 'High'
       END AS price_category
FROM pair_BTCUSDT;
```

<br />

**OVER**:

OVER: The OVER() clause is used with window functions to define the window or range of rows the function will operate on. It allows you to perform calculations across a set of table rows related to the current row. You can use it with various window functions like ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE(), LEAD(), LAG(), FIRST_VALUE(), LAST_VALUE(), and aggregate functions like SUM(), AVG(), MIN(), MAX().
Example: Calculate a simple 5 days moving average.

```sql
SELECT open_time, close,
       AVG(close) OVER (ORDER BY open_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS moving_average
FROM pair_BTCUSDT;
```

<br />

**LAG**:

LAG: The LAG() function is a window function that returns the value of a given expression for the row that is N rows before the current row within the result set. If no such row exists or the value is NULL, it returns NULL.

```sql
SELECT open_time, close, LAG(close) OVER (ORDER BY open_time) AS prev_close
FROM pair_BTCUSDT;
```

<br />

**ABS**:

ABS: The ABS() function returns the absolute value of a given numeric expression. It removes the negative sign from negative numbers, effectively returning the non-negative version of the value.

```sql
SELECT open_time, close, ABS(close - 30000) AS abs_difference
FROM pair_BTCUSDT;
```

<br />


**ROW_NUMBER**:

ROW_NUMBER: The ROW_NUMBER() function is a window function that assigns a unique, sequential integer to each row within the result set, based on the specified ORDER BY clause. It is often used to rank rows or paginate results.

```sql
SELECT open_time, close, ROW_NUMBER() OVER (ORDER BY open_time) AS row_num
FROM pair_BTCUSDT;
```

<br />
<br />

### <a id="useful-sql-commands-for-technical-analysis"></a>Useful SQL Commands for Technical Analysis

<br />

**Calculate Simple Moving Average (SMA)**:

Calculate the 200-day simple moving average for a specific trading pair.

```sql
SELECT close_time, close, volume, num_trades, 
AVG(close) OVER (ORDER BY close_time ROWS BETWEEN 199 PRECEDING AND CURRENT ROW) AS SMA_200
FROM pair_BTCUSDT
ORDER BY close_time DESC
LIMIT 200;
```

<br />

**Calculate Relative Strength Index (RSI)**:

Calculate the 14-day Relative Strength Index (RSI) for a specific trading pair.

```sql
WITH changes AS (
    SELECT
        close_time,
        close,
        close - LAG(close) OVER (ORDER BY close_time) AS price_change
    FROM pair_BTCUSDT
)
SELECT
    close_time,
    close,
    100 - (100 / (1 + (
        SUM(CASE WHEN price_change > 0 THEN price_change ELSE 0 END) OVER (ORDER BY close_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) /
        NULLIF(SUM(CASE WHEN price_change < 0 THEN ABS(price_change) ELSE 0 END) OVER (ORDER BY close_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW), 0)
    ))) AS rsi
FROM changes
ORDER BY close_time DESC
LIMIT 200;
```

<br />
<br />

### <a id="python-samples---how-to-implement-sql-in-python"></a>Python Samples - How to implement SQL in Python

#### SQL Playground: [Streamlit Cloud](https://pyfihub-streamlit-apps-streamlit-sql-db-uo2s89.streamlit.app)
<br />

```python
import sqlite3
import pandas as pd

## Open database to get list of trading pairs available.
def fetch_pairs_db():
    conn = sqlite3.connect('trading_data.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    conn.close()
    
    return tables

## Connect to table to get data for pair selected.
def fetch_data_db(symbol):
    conn = sqlite3.connect('trading_data.db')
    pair = "pair_" + symbol
    df = pd.read_sql_query(f"SELECT * FROM {pair}", conn)
    conn.close()
    
    return df

## SMA Query Test   
def submit_query(symbol):
    conn = sqlite3.connect('trading_data.db')
    pair = "pair_" + symbol
    query = f"""
    SELECT open_time, close,
           AVG(close) OVER (ORDER BY open_time ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS sma_20
    FROM {pair};
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


## Samples

# Print Pairs Tables
for item in fetch_pairs_db()[:5]:
    print(item[0])

# Print Data Sample with BTCUSDT
print(fetch_data_db("BTCUSDT").head())

# Print Query Results (SMA 20 Example)
print(submit_query("BTCUSDT").head())
```