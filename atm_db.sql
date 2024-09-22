CREATE DATABASE atm_db;

   USE atm_db;

   CREATE TABLE accounts (
    account_number VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL,
    PRIMARY KEY (account_number)
);
