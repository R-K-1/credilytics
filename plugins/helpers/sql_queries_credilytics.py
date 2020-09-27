class SqlQueriesCredilytics:
    create_accounts = f"""
        drop table if exists stage;
        create table stage (
            year int
        );
        """
    
    
    create_accounts = f"""
        drop table if exists accounts;
        create table accounts (
            year int
        );
        """

    create_delinquencies_fact = f"""
        drop table if exists delinquencies;
        create table delinquencies (
            year int
        );
        """

    create_finances_fact = f"""
        drop table if exists finances;
        create table finances (
            year int
        );
        """

    create_demographics_fact = f"""
        drop table if exists demographics;
        create table demographics (
            year int
        );
        """