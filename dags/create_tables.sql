DROP TABLE IF EXISTS public.stage;
CREATE TABLE IF NOT EXISTS public.stage (
  SeriousDlqin2yrs VARCHAR(256),
  RevolvingUtilizationOfUnsecuredLines VARCHAR(256),
  age VARCHAR(256),
  NumberOfTime3059DaysPastDueNotWorse VARCHAR(256),
  DebtRatio VARCHAR(256),
  MonthlyIncome VARCHAR(256),
  NumberOfOpenCreditLinesAndLoans VARCHAR(256),
  NumberOfTimes90DaysLate VARCHAR(256),
  NumberRealEstateLoansOrLines VARCHAR(256),
  NumberOfTime6089DaysPastDueNotWorse VARCHAR(256),
  NumberOfDependents VARCHAR(256),
  BorrowerId varchar(256) NOT NULL,
  CONSTRAINT stage_pkey PRIMARY KEY (BorrowerId)
);

DROP TABLE IF EXISTS public.accounts;
CREATE TABLE IF NOT EXISTS public.accounts (
  BorrowerId varchar(256) NOT NULL,
  CONSTRAINT accounts_pkey PRIMARY KEY (BorrowerId)
);

DROP TABLE IF EXISTS public.demographics;
CREATE TABLE IF NOT EXISTS public.demographics (
  age VARCHAR(256),
  NumberOfDependents VARCHAR(256),
  BorrowerId varchar(256) NOT NULL,
  CONSTRAINT demographics_pkey PRIMARY KEY (BorrowerId)
);

DROP TABLE IF EXISTS public.finances;
CREATE TABLE IF NOT EXISTS public.finances (
  RevolvingUtilizationOfUnsecuredLines VARCHAR(256),
  DebtRatio VARCHAR(256),
  MonthlyIncome VARCHAR(256),
  NumberOfOpenCreditLinesAndLoans VARCHAR(256),
  NumberRealEstateLoansOrLines VARCHAR(256),
  BorrowerId varchar(256) NOT NULL,
  CONSTRAINT finances_pkey PRIMARY KEY (BorrowerId)
);

DROP TABLE IF EXISTS public.delinquencies;
CREATE TABLE IF NOT EXISTS public.delinquencies (
  SeriousDlqin2yrs VARCHAR(256) NOT NULL,
  NumberOfTime3059DaysPastDueNotWorse SMALLINT,
  NumberOfTimes90DaysLate SMALLINT,
  NumberOfTime6089DaysPastDueNotWorse SMALLINT,
  BorrowerId varchar(256) NOT NULL,
  CONSTRAINT delinquencies_pkey PRIMARY KEY (BorrowerId)
);

