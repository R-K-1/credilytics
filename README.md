# Credilytics

_Credilytics_ is intended to demonstrate how to design and implement a data warehouse
and an ETL data pipeline using Python, Spark, Airflow, S3 and Postgres (Redshift cluster)

## Purpose

The purpose of this project is to provide credit risk analysts with a public database
they can query to fine tune the rules used to give credit to applicants
based on demongraphics, financial and delinquencies information of current borrowers.

The following are some questions that can be answered by the data:

* How many percent of borrowers under 30 years old have have had a serious delinquency?
* What is the average number of loans and open credit lines for homeowners?
* How many percent of borrowers with two or more dependents have had a 30-59 days delinquency?
* What is the average household income of borrowers with a 60-89 days delinquency?

## Setup

* Download `cs-training.csv` dataset and then upload it to `<s3-bucket-name>/input`
* Create `<s3-bucket-name>/staging` folder
* Set up a Redshift Cluster with the permission to read from S3
* Set up Apache Airflow
* Set up Spark
* Install Pyspark Python module
* Create the following `Connections` in Airflow
	* `redshift` : with the information necessary to connect to a redshift cluster
    * `aws_credentials` : with the credentials for an IAM user able to read and write to `<s3-bucket-name>`
* Create the following `Variables` in Airflow
	* `bucket_name` : with the name of the bucket where the input data is uploaded and the stage data will be written
    * `number_of_rows`: the data quality checks needs this variable

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

This project generates five tables in a Postgres database:

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

### Source Code

```bash
├── README.md - This file.
├── dags
	└── credilitycs.py # Python script containing the tasks and depencdencies of the DAG
├── plugins
	├── helpers
		├── __init__.py
		├── sql_queries.py # Defining prepared and reusable SQL queries
    ├── operators
		├── __init__.py
		├── data_quality.py # with `DataQualityOperator`, running data quality check by passing an array of SQL queries and an expected result as arguments, failing if the result of any query does not match the expected one.
		├── load.py # with `LoadOperator`, loading a dimension or fact table from data in the stage table.
		├── transform.py # with `TransformOperator`, loading the original CSV into a DataFrame, appending a UUID to each row and saving the result in parquet format.
		└── stage_redshift.py # with `StageToRedshiftOperator`, Loading the parquet datda into the stage table of the data warehouse inside the Redshift cluster
```

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

Eventually this project may have to address the following scenarios as it grows and evolves in its use:

* **The ETL process needs to be completed faster** The intermediate step storing the data in parquet may need to be eliminated and the data uploaded directly to the warehouse
* **The pipelines would be run on a daily basis by 7am every day.** The parameters in the DAG would have to be changed to run at a higher frequency (using the `schedule_interval` parameter), which also may entail having to increasing the maximum number of concurrent DAG runs if each run takes longer than a day.

## Example Queries

**How many percent of customers under 30 years old have have had a serious delinquency?**

```
SELECT b.BorrowerId
FROM borrowers b
INNER JOIN delinquencies d
ON b.BorrowerId=d.BorrowerId
AND d.SeriousDlqin2yrs = '1'
LIMIT 10
```

**What is the average number of loans and open credit lines for homeowners?**

```
SELECT AVG(f.NumberOfOpenCreditLinesAndLoans)
FROM finances f
WHERE f.NumberRealEstateLoansOrLines > 0
```

**How many percent of customers with two or more dependents have had a 30-59 days delinquency?**

```
SELECT ROUND(
  100.0 * (
      SUM(CASE WHEN (dem.NumberOfDependents > 1 AND del.NumberOfTime3059DaysPastDueNotWorse > 0) THEN 1 ELSE 0 END) / 
    		COUNT(CASE WHEN (dem.NumberOfDependents > 1) THEN 1 ELSE 0 END)
	), 1) AS percent_total
FROM demographics dem
INNER JOIN delinquencies del
ON dem.BorrowerId=del.BorrowerId
```

**What is the average household income of customers with a 60-89 days delinquency?**

```
SELECT AVG(f.MonthlyIncome)
FROM finances f
INNER JOIN delinquencies d
ON f.BorrowerId = d.BorrowerId
```