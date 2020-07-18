# Project: Data Modeling with Postgres


## Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis. Therefore the goal of this project is to create a database schema and ETL pipeline for this analysis. 


## 1. Database Design Description
There are two source datasets, one called "song" and another "log". And from these two datasetes the following star schema database will been created for optimized queries on song play analysis. The tables are as below:

### 1.1 Fact Table
The fact table in this star scheme will be named "songplays" and is designed to record "log" data associated with song plays. This fact table will have the
following columns: songplay_id (PK), start_time (FK), user_id (FK), level, song_id (FK), artist_id (FK), session_id, location, user_agent. NOTE: PK denotes
PRIMARY KEY and FK denotes FORIEGN KEY.
### 1.2 Dimension Tables
The following tables in this star scheme are all dimension tables.
- users - This table will be used to record unique user details. This table will have the following columns:
            user_id (PK), first_name, last_name, gender, level.
- songs - This table will be used to record unique song details. This table will have the following columns:
            song_id (PK), title, artist_id, year, duration.
- artists - This table will be used to record unique artist details. This table will have the following columns:
            artist_id (PK), name, location, latitude, longitude.
- time - This table will be used to record unique time details. This table will have the following columns: 
            start_time (PK), hour, day, week, month, year, weekday


## 2. Files in the repository
There are two source datasets, one called "song" and another "log" and these are locationed in the data/song_data and data/log_data respectively. The subsections below 

### 2.1 create_tables.py
This script does the following:
- Drops (if exists) and Creates the sparkify database. 
- Establishes connection with the sparkify database and gets cursor to it.  
- Drops all the tables (by calling the script "sql_queries".  
- Creates all tables needed. 
- Finally, closes the connection.

### 2.2 sql_queries.py
This script does the following:  
- Drops (if exists) all the tables once called by the script "create_tables".  
- Creates all tables once called by the script "create_tables".
- Insert records into tables extracted from the source datasets.

### 2.3 etl.ipynb
This jupyter notedbook was used to develop the code used in the "etl.py" script.

### 2.4 test.ipynb
This jupyter notedbook was used to test that the code developed in "etl.ipynb" performs as expected and populates the intended tables with the correct information.

### 2.5 etl.py
This script does the following:  
- Extracts, transforms and loads data into the tables already created in by the "create_tables.py" script. 

### 2.6 dashboard.ipynb
Dashboard containing 3 figures track slightly different things:
- High Usage User Tracker - The SQL query that supports this visulisation filters our users that have returned to the service more than 10 times. The intention of this graph is to track high usage returning users.
- Playsong Count - Tracks the total "Playcounts" per week of the year, intention is to track the real overall usage of the service.
- Figure 3 - This jointplot is another usage tracker but with a variance to show how usage is evolving throughout the day.

## 3. User Guide
To populated the tables with the data from the source datasets the following scripts "create_tables.py" and "etl.py" will have to be ran in sequence respectively in a terminal window, as per below:
- Type the following into the terminal window "Python create_tables.py", followed by the return key.
- Type the following into the terminal window "Python etl.py", followed by the return key.

After following the above two commands the database will be populated with the source data and ready for queries to be performed to extract the necessary data for analysis.