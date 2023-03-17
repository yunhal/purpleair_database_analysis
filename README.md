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


#### About the scripts 

**You must have the followings before executing the script:**
- purpleair_api_read_key : a text file in the working directory that contains your PurpleAir API key 
- sensor_id : a parameter in the script for a sensor ID (e.g., sensor_id = '143856') 
- Install the required packages (see the package list in the purpleair_build_database.py) 


**purpleair_build_database.py** - to create sqlite and csv database 

>>You will need to run this python script in the background in a computer, which must be turned on all the times to avoid any data loss. 
>> To avoid overwriting the existing data files accidentally, the database directory is created with the datetime you executed the python script. 

```
python purpleair_build_database.py &
```

**purpleair_build_database_test.ipynb** - to check how the script works (it creates the database files with only the first data) 

**test_reading_sqlite_csv.ipynb** - to check saved PA data in the database files. 

