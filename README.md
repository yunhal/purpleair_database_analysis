## Building a SQL and CSV database for PurpleAir

#### Author: Yunha Lee, Ph.D. 
#### Date  : March 01, 2023

The code below is designed to create a database using SQLite and CSV files in your local computer. It takes real-time data from a PurpleAir (PA) sensor and stores them under the database directory.  Recently PurpleAir limits public access to their historical database (read below for more information), so this allows to build your own historical database.

* It uses the "purpleair" library from GitHub, which handles Purple Air API: https://github.com/csm10495/purpleair

##### Side Note about PurpleAir database

PurpleAir has recently changed the database access methods.  

As of December, 2022, the recommended methods to get PurpleAir data are the below:

1) using their "Sensor data download tool" website (without API)
    see link: https://www.purpleair.com/sensorlist
2) using real-time API to create your own "personal" database, instead of using their historical API
    see link: https://community.purpleair.com/t/historical-api-endpoints-are-now-restricted/1557
3) using the historical API occasionally to get the missed data
    email contact@purpleair.com to get a permission to use the history API. 

*This code is designed to support the method "2", building your own database in a local computer.*


#### How to use 

You will need to run this python script in the background in a computer, which must be turned on all the times to avoid any data loss. 

```
python purpleair_build_database.py &
```

To avoid overwriting the existing data files accidentally, the database directory is created with the date you executed the python script. 