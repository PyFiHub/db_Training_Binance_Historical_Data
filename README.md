# db_Training_Binance_Historical_Data
 SQL and Python Practice - Coin/Token Binance

## Summary

- [Binance Historical Data](#binance-historical-data)
- [Useful SQL Commands for Data Analysis](#useful-sql-commands-for-data-analysis)
- [Useful SQL Commands for Technical Analysis](#useful-sql-commands-for-technical-analysis)
- [Python Samples - How to implement SQL in Python](#python-samples---how-to-implement-sql-in-python)


<br />
<br />

### <a id="binance-historical-data"></a>Binance Historical Data

This script [main.py](https://github.com/PyFiHub/db_Training_Binance_Historical_Data/blob/main/main.py) imports historical trading data for multiple cryptocurrency pairs from the Binance API, processes the data, and stores it in an SQLite database. Let's break down the different parts of the code:

- **Libraries**: Import necessary libraries for the script, including requests for HTTP requests, pandas for data manipulation, logging for logging messages, Binance client for interacting with Binance API, and sqlite3 for working with SQLite databases.

- **Binance Client**: Initialize the Binance client with API key and secret from the api_keys module.

- **Logger**: Set up the logger to handle logging messages with the specified format.

- **Functions**:
    - `convert_to_float()`: Converts specific columns in the given DataFrame to float data type.
    - `get_trading_pairs()`: Retrieves a list of trading pairs from the Binance API. It filters the list to include only pairs with a status of "TRADING" and having "USDT" in their symbol.
    - `get_historical_data()`: Gets historical trading data for a specified trading pair, given the latest timestamp recorded in the database, the interval for the data, and the number of data points to retrieve. It drops unnecessary columns, converts specific columns to float data type, and converts the "open_time" and "close_time" columns to datetime objects. It then filters the data based on the latest timestamp, if provided.
    - `create_table()`: Creates a table in the SQLite database for each trading pair, with a specified structure for storing historical trading data.

- **Main script**:
    - Get the list of trading pairs by calling `get_trading_pairs()`.
    - If there are trading pairs, connect to the SQLite database, trading_data.db.
    - For each trading pair, create a table in the database, log the trading pair being added, and retrieve the latest timestamp recorded in the table.
    - Get the historical data for the trading pair with the latest timestamp, if it exists.
    - If the retrieved data is not empty, append the new data to the corresponding table in the database.
    - If an error occurs while retrieving data for a trading pair, log the error message.

This script ensures that only new historical trading data is added to the database each time it is run, avoiding duplication of data.

<br />
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

**COALESCE**:

COALESCE: The COALESCE() function returns the first non-null value in a list of expressions. It is often used to replace null values with a default value or another column's value.

```sql
SELECT open_time, COALESCE(volume, 0) AS volume
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

**STDDEV_POP**:

STDDEV_POP: The STDDEV_POP() function is an aggregate function that returns the population standard deviation of a given expression. It calculates the square root of the variance, which is the average of the squared differences from the mean.

```sql
SELECT open_time, close,
       STDDEV_POP(close) OVER (ORDER BY open_time ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS stddev_20
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

Calculate the 20-day simple moving average for a specific trading pair.

```sql
SELECT open_time, close,
       AVG(close) OVER (ORDER BY open_time ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS sma_20
FROM pair_BTCUSDT;
```

<br />

**Calculate Bollinger Bands**:

Calculate the 20-day Bollinger Bands, which include the upper and lower bands based on the simple moving average and standard deviation.

```sql
SELECT open_time, close, sma_20,
       sma_20 + 2 * stddev_20 AS upper_band,
       sma_20 - 2 * stddev_20 AS lower_band
FROM (
    SELECT open_time, close,
           AVG(close) OVER (ORDER BY open_time ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS sma_20,
           STDDEV_POP(close) OVER (ORDER BY open_time ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS stddev_20
    FROM pair_BTCUSDT
) sub;
```

<br />

**Calculate Relative Strength Index (RSI)**:

Calculate the 14-day Relative Strength Index (RSI) for a specific trading pair.

```sql
WITH gains_losses AS (
    SELECT open_time, close,
           COALESCE(close - LAG(close) OVER (ORDER BY open_time), 0) AS change
    FROM pair_BTCUSDT
),
gain_loss_sums AS (
    SELECT open_time, close,
           SUM(CASE WHEN change >= 0 THEN change ELSE 0 END) OVER (ORDER BY open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS gain_sum,
           SUM(CASE WHEN change < 0 THEN ABS(change) ELSE 0 END) OVER (ORDER BY open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS loss_sum
    FROM gains_losses
)
SELECT open_time, close,
       100 - (100 / (1 + (gain_sum / loss_sum))) AS rsi_14
FROM gain_loss_sums;
```

<br />
<br />

### <a id="python-samples---how-to-implement-sql-in-python"></a>Python Samples - How to implement SQL in Python

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