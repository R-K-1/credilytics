class SqlQueries:
    create_tables = ("""
        DROP TABLE IF EXISTS public.stage;
        CREATE TABLE IF NOT EXISTS public.stage (
            SeriousDlqin2yrs varchar(256) NOT NULL,
            RevolvingUtilizationOfUnsecuredLines varchar(256) NOT NULL,
            age varchar(256) NOT NULL,
            NumberOfTime30-59DaysPastDueNotWorse varchar(256) NOT NULL,
            DebtRatio varchar(256) NOT NULL,
            MonthlyIncome varchar(256) NOT NULL,
            NumberOfOpenCreditLinesAndLoans varchar(256) NOT NULL,
            NumberOfTimes90DaysLate varchar(256) NOT NULL,
            NumberRealEstateLoansOrLines varchar(256) NOT NULL,
            NumberOfTime60-89DaysPastDueNotWorse varchar(256) NOT NULL,
            NumberOfDependents varchar(256) NOT NULL,
            AccountId varchar(256) NOT NULL,
            CONSTRAINT stage_pkey PRIMARY KEY (AccountId)
        );
    """)
    
    create_stage = ("""
        drop table if exists stage;
        create table stage (
            year int
        );
        """)
    
    
    create_accounts = ("""
        drop table if exists accounts;
        create table accounts (
            year int
        );
        """)

    create_delinquencies_fact = ("""
        drop table if exists delinquencies;
        create table delinquencies (
            year int
        );
        """)

    create_finances_fact = ("""
        drop table if exists finances;
        create table finances (
            year int
        );
        """)

    create_demographics_fact = ("""
        drop table if exists demographics;
        create table demographics (
            year int
        );
        """)