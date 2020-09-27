DROP TABLE IF EXISTS public.stage;
CREATE TABLE IF NOT EXISTS public.stage (
  SeriousDlqin2yrs BOOLEAN NOT NULL,
  RevolvingUtilizationOfUnsecuredLines NUMERIC(15, 10),
  age SMALLINT,
  NumberOfTime3059DaysPastDueNotWorse SMALLINT,
  DebtRatio NUMERIC(15, 10),
  MonthlyIncome SMALLINT,
  NumberOfOpenCreditLinesAndLoans SMALLINT,
  NumberOfTimes90DaysLate SMALLINT,
  NumberRealEstateLoansOrLines SMALLINT,
  NumberOfTime6089DaysPastDueNotWorse SMALLINT,
  NumberOfDependents SMALLINT,
  AccountId varchar(256) NOT NULL,
  CONSTRAINT stage_pkey PRIMARY KEY (AccountId)
);

DROP TABLE IF EXISTS public.accounts;
CREATE TABLE IF NOT EXISTS public.accounts (
  AccountId varchar(256) NOT NULL,
  CONSTRAINT accounts_pkey PRIMARY KEY (AccountId)
);

DROP TABLE IF EXISTS public.demographics;
CREATE TABLE IF NOT EXISTS public.demographics (
  age SMALLINT,
  NumberOfDependents SMALLINT,
  AccountId varchar(256) NOT NULL,
  CONSTRAINT demographics_pkey PRIMARY KEY (AccountId)
);

DROP TABLE IF EXISTS public.finances;
CREATE TABLE IF NOT EXISTS public.finances (
  RevolvingUtilizationOfUnsecuredLines NUMERIC(15, 10),
  DebtRatio NUMERIC(15, 10),
  MonthlyIncome SMALLINT,
  NumberOfOpenCreditLinesAndLoans SMALLINT,
  NumberRealEstateLoansOrLines SMALLINT,
  AccountId varchar(256) NOT NULL,
  CONSTRAINT finances_pkey PRIMARY KEY (AccountId)
);

DROP TABLE IF EXISTS public.delinquencies;
CREATE TABLE IF NOT EXISTS public.delinquencies (
  SeriousDlqin2yrs BOOLEAN NOT NULL,
  NumberOfTime3059DaysPastDueNotWorse SMALLINT,
  NumberOfTimes90DaysLate SMALLINT,
  NumberOfTime6089DaysPastDueNotWorse SMALLINT,
  AccountId varchar(256) NOT NULL,
  CONSTRAINT delinquencies_pkey PRIMARY KEY (AccountId)
);

