import pandas as pd
import pyodbc
from pd_to_mssql import to_sql

cnxn_ED_stg = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=oh01msvsp64.workflowone.net\proddas1;Database=EnterpriseDataStage;Trusted_Connection=yes;')
cnxn_ED = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=oh01msvsp64.workflowone.net\proddas1;Database=EnterpriseData;Trusted_Connection=yes;')
lrd_cnxn_string = 'Driver={ODBC Driver 17 for SQL Server};Server=TCSQL4D;Database=LabelRevenueData;Trusted_Connection=yes;'
lrd_cnxn = pyodbc.connect(lrd_cnxn_string)
lrd_crsr = lrd_cnxn.cursor()
CA_CHQ_cnxn_string = 'Driver={ODBC Driver 17 for SQL Server};Server=CHQSQL2;Database=CUR_Shipped_Sales;UID=TcAnalytics;PWD=TcAnalytics;'
CA_CATL_cnxn_string = 'Driver={ODBC Driver 17 for SQL Server};Server=CATLSQLCorpProd;Database=Sales_Org;UID=TcAnalytics;PWD=TcAnalytics;'
df_enterprise_customers = pd.read_sql('SELECT * FROM [EnterpriseData].[dbo].[Customers] WHERE Company_Nbr IN (222, 224) and curr_ind = 1', cnxn_ED)
to_sql(df_enterprise_customers, 'EnterpriseDataCustomers', lrd_cnxn_string, index=False, replace=True)