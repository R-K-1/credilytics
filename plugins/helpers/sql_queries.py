class SqlQueries:
    create_tables = ("""
        DROP TABLE IF EXISTS public.stage;
        CREATE TABLE IF NOT EXISTS public.stage (
            SeriousDlqin2yrs VARCHAR(100),
            RevolvingUtilizationOfUnsecuredLines VARCHAR(100),
            age VARCHAR(100),
            NumberOfTime3059DaysPastDueNotWorse VARCHAR(100),
            DebtRatio VARCHAR(100),
            MonthlyIncome VARCHAR(100),
            NumberOfOpenCreditLinesAndLoans VARCHAR(100),
            NumberOfTimes90DaysLate VARCHAR(100),
            NumberRealEstateLoansOrLines VARCHAR(100),
            NumberOfTime6089DaysPastDueNotWorse VARCHAR(100),
            NumberOfDependents VARCHAR(100),
            BorrowerId BIGINT NOT NULL,
            CONSTRAINT stage_pkey PRIMARY KEY (BorrowerId)
        );

        DROP TABLE IF EXISTS public.borrowers;
        CREATE TABLE IF NOT EXISTS public.borrowers (
            BorrowerId BIGINT NOT NULL,
            CONSTRAINT accounts_pkey PRIMARY KEY (BorrowerId)
        );

        DROP TABLE IF EXISTS public.demographics;
        CREATE TABLE IF NOT EXISTS public.demographics (
            age VARCHAR(100),
            NumberOfDependents VARCHAR(100),
            BorrowerId BIGINT NOT NULL,
            CONSTRAINT demographics_pkey PRIMARY KEY (BorrowerId)
        );

        DROP TABLE IF EXISTS public.finances;
        CREATE TABLE IF NOT EXISTS public.finances (
            RevolvingUtilizationOfUnsecuredLines VARCHAR(100),
            DebtRatio VARCHAR(100),
            MonthlyIncome VARCHAR(100),
            NumberOfOpenCreditLinesAndLoans VARCHAR(100),
            NumberRealEstateLoansOrLines VARCHAR(100),
            BorrowerId BIGINT NOT NULL,
            CONSTRAINT finances_pkey PRIMARY KEY (BorrowerId)
        );

        DROP TABLE IF EXISTS public.delinquencies;
        CREATE TABLE IF NOT EXISTS public.delinquencies (
            SeriousDlqin2yrs VARCHAR(100),
            NumberOfTime3059DaysPastDueNotWorse VARCHAR(100),
            NumberOfTimes90DaysLate VARCHAR(100),
            NumberOfTime6089DaysPastDueNotWorse VARCHAR(100),
            BorrowerId BIGINT NOT NULL,
            CONSTRAINT delinquencies_pkey PRIMARY KEY (BorrowerId)
        );
    """)
    
    borrowers_table_insert = ("""
        SELECT BorrowerId
        FROM stage
        """)    
    
    demographics_table_insert = ("""
        SELECT age, NumberOfDependents, BorrowerId
        FROM stage
        """)

    finances_table_insert = ("""
        SELECT RevolvingUtilizationOfUnsecuredLines, DebtRatio, MonthlyIncome,
            NumberOfOpenCreditLinesAndLoans, NumberRealEstateLoansOrLines,BorrowerId
        FROM stage
        """)

    delinquencies_tables_insert = ("""
        SELECT SeriousDlqin2yrs, NumberOfTime3059DaysPastDueNotWorse, NumberOfTimes90DaysLate,
            NumberOfTime6089DaysPastDueNotWorse, BorrowerId
        FROM stage
        """)
    
    data_quality_check_queries = [
        'SELECT COUNT(BorrowerId) FROM stage',
        'SELECT COUNT(BorrowerId) FROM borrowers',
        'SELECT COUNT(BorrowerId) FROM demographics',
        'SELECT COUNT(BorrowerId) FROM finances',
        'SELECT COUNT(BorrowerId) FROM delinquencies']