# Credilytics

_Credilytics_ is intended to demonstrate how to design and implement a data warehouse
and an ETL data pipeline using Python, Spark, Airflow, S3 and Postgres (Redshift cluster)

## Purpose

The purpose of this project is to provide credit risk analysts with a public database
they can easily query and analyze to fine tune the rules used to give credit to applicants
based on demongraphics, financial and delinquencies information of current accounts.

The following are some questions that can be asked with the data:

* How many percent of customers under 30 years old have have had a serious delinquency?
* What is the average number of loans and open credit lines for homeowners?
* How many percent of customers with two or more dependents have had a 30-59 days delinquency?
* What is the average household income of customers with a 60-89 days delinquency?

## Setup
## TODO

## Source Data

This project draws on historical borrowers data provided for a Kaggle competition
aiming to build an algorithm predicting the likelihood of a borrower experiencing
financial hardship. [Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit/overview)

**Give Me Some Credit Training Data**

* Name: _cs-training.csv_
* Location: [cs-training.csv](https://www.kaggle.com/c/GiveMeSomeCredit/data?select=cs-training.csv)
* Update frequency: None
* Number of rows (as of Sep 27 2020): 150,000
* Description: demographic, financial and delinquency information for borrowers including whether or not they experienced a 90 days past due delinquency

## Data Model

This project generates 5 tables in a Postgres database:

1. `stage`: all data is loaded here first for rapid insertion into other tables
    * `SeriousDlqin2yrs`: Person experienced 90 days past due delinquency or worse 
    * `RevolvingUtilizationOfUnsecuredLines`: Total balance on credit cards and personal lines of credit except real estate and no installment debt like car loans divided by the sum of credit limits
    * `age`: Age of borrower in years
    * `NumberOfTime3059DaysPastDueNotWorse`: Number of times borrower has been 30-59 days past due but no worse in the last 2 years.
    * `DebtRatio`: Monthly debt payments, alimony,living costs divided by monthy gross income
    * `MonthlyIncome`: Monthly income
    * `NumberOfOpenCreditLinesAndLoans`: Number of Open loans (installment like car loan or mortgage) and Lines of credit (e.g. credit cards)
    * `NumberOfTimes90DaysLate`: Number of times borrower has been 90 days or more past due.
    * `NumberRealEstateLoansOrLines`: Number of mortgage and real estate loans including home equity lines of credit
    * `NumberOfTime6089DaysPastDueNotWorse`: Number of times borrower has been 60-89 days past due but no worse in the last 2 years.
    * `NumberOfDependents`: Number of dependents in family excluding themselves (spouse, children etc.)
    * `BorrowerId`: identifier generated during transformation

2. `borrowers`: facts table storing the Id of each borrower
    * `BorrowerId`: identifier generated during transformation
    
3. `demographics`: demographic information of each borrower
    * `age`: Age of borrower in years
    * `NumberOfDependents`: Number of dependents in family excluding themselves (spouse, children etc.)
    * `BorrowerId`: identifier generated during transformation
    
4. `finances`: financial information of each borrower
    * `RevolvingUtilizationOfUnsecuredLines`: Total balance on credit cards and personal lines of credit except real estate and no installment debt like car loans divided by the sum of credit limits
    * `DebtRatio`: Monthly debt payments, alimony,living costs divided by monthy gross income
    * `MonthlyIncome`: Monthly income
    * `NumberOfOpenCreditLinesAndLoans`: Number of Open loans (installment like car loan or mortgage) and Lines of credit (e.g. credit cards)
    * `NumberRealEstateLoansOrLines`: Number of mortgage and real estate loans including home equity lines of credit
    * `BorrowerId`: identifier generated during transformation
    
5. `delinquencies`: delinquency information of each borrower
    * `SeriousDlqin2yrs`: Person experienced 90 days past due delinquency or worse 
    * `NumberOfTime3059DaysPastDueNotWorse`: Number of times borrower has been 30-59 days past due but no worse in the last 2 years.
    * `NumberOfTimes90DaysLate`: Number of times borrower has been 90 days or more past due.
    * `NumberOfTime6089DaysPastDueNotWorse`: Number of times borrower has been 60-89 days past due but no worse in the last 2 years.
    * `BorrowerId`: identifier generated during transformation


## Project Structure

### ETL

* Spark used Pandas to read input CSV from S3 into a DataFrame
* An unique identifier is added to each record
* The resulting dataframe is written to S3 staging area in parquet format
* The staged data are loaded into the staging table in Postgres DB inside the Redshift cluster
* Data is copied from from the staging table to the different facts and dimentions table of the star schema
* Data quality checks are run, including ensuring that the number for rows in each table is the same and is equal to the number of rows in the original CSV
* All operations are orchestrated by Airflow via a dag and its tasks

### Tools

* **Python** is used as the programming language because of its ease-of-use and flexibility
* **S3** is used as the input and transform staging area because of its scalability, durability and support of multiple file formats
* **Spark** (specfically **PySpark**) is used to transform the data because of its ability to handle big data sets
* **Airflow** is used to orchestrate the steps of the ETL data pipeline because of its powerful scheduling and monitoring features
* **Redshift** is used to host the data warehouse because of its ability to handle OLAP for big data

## Potential Scenarios
## TODO

Eventually this project may have to address the following scenarios as it grows and evolves in its use:

## Example Queries
## TODO