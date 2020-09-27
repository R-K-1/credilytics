DROP TABLE IF EXISTS public.stage;

CREATE TABLE IF NOT EXISTS public.stage (
  SeriousDlqin2yrs varchar(256) NOT NULL,
  RevolvingUtilizationOfUnsecuredLines varchar(256) NOT NULL,
  age varchar(256) NOT NULL,
  NumberOfTime3059DaysPastDueNotWorse varchar(256) NOT NULL,
  DebtRatio varchar(256) NOT NULL,
  MonthlyIncome varchar(256) NOT NULL,
  NumberOfOpenCreditLinesAndLoans varchar(256) NOT NULL,
  NumberOfTimes90DaysLate varchar(256) NOT NULL,
  NumberRealEstateLoansOrLines varchar(256) NOT NULL,
  NumberOfTime6089DaysPastDueNotWorse varchar(256) NOT NULL,
  NumberOfDependents varchar(256) NOT NULL,
  AccountId varchar(256) NOT NULL,
  CONSTRAINT stage_pkey PRIMARY KEY (AccountId)
);