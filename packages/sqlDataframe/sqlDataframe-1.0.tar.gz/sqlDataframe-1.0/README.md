# sqlDataframe

SQL To Pandas is a tool you can use to connect with your database, somme of the basic Functionalities are:

  - Can convert your database table into pandas dataframe
  - You can insert a pandas dataframe as a new table into your database

Usage pattern is different for both linux and windows.

# Linux
#### Quickstart
Installing dependencies first:
```sh
$ import pandas as pd
$ from sqlDataframe import sqlCred, read_sql, to_sql
```
Establishing connection and importing data from mssql server into Pandas dataframe:
```sh
$ creds = sqlCred(database='database_name', username='username', password='pass', OS='Linux')
$ dataframe = read_sql(creds,'table_name')
```
Establishing connection and importing data Pandas dataframe into mssql server:
```sh
$ creds = to_sql(database='database_name', username='username', password='pass', OS='Linux')
$ to_sql(creds, dataframe, 'table_name')
```
Once  connection is establised, you can use **creds** for both **read_sql** and **to_sql**.

# Windows
#### Quickstart
Installing dependencies first:
```sh
$ import pandas as pd
$ from sqltopandas import sqlCred, to_sql, read_sql
```

Establishing connection and importing data from mssql server into Pandas dataframe:
```sh
$ creds = sqlCred('database='database_name', server='server_name', OS='Windows')
$ dataframe = read_sql(creds,'table_name')
```

Establishing connection and importing data Pandas dataframe into mssql server:
```sh
$ creds = sqlCred('database='database_name', server='server_name', OS='Windows')
$ to_sql(creds, dataframe, 'table_name')
```

Once  connection is establised, you can use **creds** for both **read_sql** and **to_sql**.
**Note:** This is only accessible using Microsoft Sql Server windows authentication.

# Upcommings
Its a start of our journey and every journey begins with some simple steps. So we have enlisted some more features to be the part of **sqltopandas** in future updates. 

  - Integration with multiple database platforms
  - Load specific data into dataframe from databasse by using custom queries
  - Server name will automatically be fetched from the system (Windows only)
  - Will provide access through sql server authentication (windows only) 

# Limitations
Yes we do have some limitations and we are working over it:

* Support with sql server authentication is not available right now (windows only)
* Only SELECT and INSERT querrying is working at the backend.
* User's custom queries will be entetained.
* Sql server instance name have to be provided as a parameter to build connection, in future we will fetch it by ourself.
