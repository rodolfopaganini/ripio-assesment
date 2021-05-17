# Assesment test for Ripio

## Task description

Suppose we have these tables:
```SQL
CREATE TABLE users (
    id INTEGER PRIMARY KEY NOT NULL, -- this is the client's id
    name VARCHAR(100) NOT NULL, -- this is the client's username
    country VARCHAR(2) -- A 2-letter country code: e.g "AR", "BR", "MX", etc
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL, -- this is the transaction amount
    product VARCHAR(20) NOT NULL, -- name of product the user bought
    txn_type VARCHAR(4) NOT NULL, -- one of "BUY" (user bought something), or "SELL" (user sold something)
    timestamp DATETIME NOT NULL, -- when the user performed the transaction
    user_id INTEGER NOT NULL, -- who performed the transaction
    FOREIGN KEY(user_id) REFERENCES users(id)
)
```

**Question 1**. how would you construct a query that shows the transaction with the lowest and
highest amount for each user?

**Question 2**. how would you construct a query that shows the average total_amount for all
transactions of each country?

**Question 3**. Create a small flask web service with 2 rest endpoints:
- endpoint #1: receives all the transaction fields except:
the transaction id, and the timestamp (you can use now())
and saves it into a database.
- endpoint #2: receives a user id, and return the sum of total_amount of that user.

Your rest service does not need to implement authentication or anything else but these 2
endpoints. The code, however, needs to run.
  
You can use any database you want (eg. sqlite), whatever makes your code simpler.

## Database setup

I'm using MySQL and for setting up the database I ran the following commands:

```SQL
CREATE DATABASE ripioDb;
USE ripioDb;

CREATE TABLE users (
    id INTEGER PRIMARY KEY NOT NULL, -- this is the client's id
    name VARCHAR(100) NOT NULL, -- this is the client's username
    country VARCHAR(2) -- A 2-letter country code: e.g "AR", "BR", "MX", etc
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL, -- this is the transaction amount
    product VARCHAR(20) NOT NULL, -- name of product the user bought
    txn_type VARCHAR(4) NOT NULL, -- one of "BUY" (user bought something), or "SELL" (user sold something)
    timestamp DATETIME NOT NULL, -- when the user performed the transaction
    user_id INTEGER NOT NULL, -- who performed the transaction
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO users (id, name, country) VALUES
  ( 10, 'Rodolfo', 'AR' ),
  ( 12, 'Irina', 'BR' ),
  ( 16, 'Miguel', 'AR' );

INSERT INTO transactions (id, total_amount, product, txn_type, timestamp, user_id) VALUES
  ( 1, 46, 'socks', 'BUY', '2021-05-05', 10),
  ( 2, 50, 'shoes', 'BUY', '2021-05-08', 12),
  ( 3, 2, 'tie', 'SELL', '2021-05-04', 16),
  ( 4, 25, 'shirt', 'BUY', '2021-05-07', 16),
  ( 5, 67, 'hat', 'BUY', '2021-05-02', 16),
  ( 6, 82, 'shoes', 'SELL', '2021-05-05', 12),
  ( 7, 93, 'socks', 'BUY', '2021-05-03', 12),
  ( 8, 5, 'shoes', 'BUY', '2021-05-07', 12);


CREATE USER 'newUser'@'localhost' IDENTIFIED BY 'newUserPass';
GRANT ALL PRIVILEGES ON *.* TO 'newUser'@'localhost';
```

## Solutions

### First query: show the transaction with the lowest and highest amount for each user

```SQL
SELECT a.*
FROM transactions a
INNER JOIN (
    SELECT user_id, MIN(total_amount) as min_amount, MAX(total_amount) as max_amount
    FROM transactions
    GROUP BY user_id
) b ON a.user_id = b.user_id AND (a.total_amount = b.min_amount OR a.total_amount = b.max_amount);
```

### Second query: show the average total_amount for all transactions of each country

```SQL
SELECT AVG(total_amount) as avg_amount, b.country
FROM transactions a
LEFT JOIN users b ON a.user_id = b.id
GROUP BY b.country;
```

### Flask web service implementation:

Find the implementation in the [main file](https://github.com/rodolfopaganini/ripio-assesment/blob/main/main.py).
