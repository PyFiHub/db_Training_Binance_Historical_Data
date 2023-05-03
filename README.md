# db_Training_Binance_Historical_Data
 SQL and Python Practice - Coin/Token Binance

### Binance Historical Data

This script imports historical trading data for multiple cryptocurrency pairs from the Binance API, processes the data, and stores it in an SQLite database. Let's break down the different parts of the code:

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

### Useful SQL Commands for Data Analysts

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
    
These aggregate functions are used to compute the average (AVG), minimum (MIN), maximum (MAX), and sum (SUM) of a set of records.Example: Calculate the average, minimum, and maximum closing prices, and the total volume for the "pair_BTCUSDT" table.

```sql
SELECT AVG(close) AS average_close, MIN(close) AS min_close, MAX(close) AS max_close, SUM(volume) AS total_volume
FROM pair_BTCUSDT;
```

<br />

**GROUP BY**:

The GROUP BY clause is used to group rows with the same values in specified columns into groups, like when using aggregate functions.Example: Calculate the average closing price for each day in the "pair_BTCUSDT" table.

```sql
SELECT DATE(open_time) AS date, AVG(close) AS average_close
FROM pair_BTCUSDT
GROUP BY date;
```

<br />

**HAVING**:

The HAVING clause is used to filter the results of a GROUP BY query, based on a condition that applies to the aggregated data.Example: Find the days where the average closing price was greater than 50000 in the "pair_BTCUSDT" table.

```sql
SELECT DATE(open_time) AS date, AVG(close) AS average_close
FROM pair_BTCUSDT
GROUP BY date
HAVING average_close > 50000;
```
