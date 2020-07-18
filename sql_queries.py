# DROP TABLES
songplay_table_drop = ("""DROP TABLE IF EXISTS songplay;""")
user_table_drop = ("""DROP TABLE IF EXISTS users;""")
song_table_drop = ("""DROP TABLE IF EXISTS song;""")
artist_table_drop = ("""DROP table IF EXISTS artist;""")
time_table_drop = ("""DROP table IF EXISTS time;""")


# CREATE TABLES
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (songplay_id int NOT NULL, 
                                        start_time timestamp NOT NULL,
                                        user_id int NOT NULL,
                                        level levels NOT NULL,
                                        song_id varchar,
                                        artist_id varchar,
                                        session_id int NOT NULL,
                                        location varchar NOT NULL,
                                        user_agent varchar NOT NULL,
                                        PRIMARY KEY (songplay_id),
                                        FOREIGN KEY (song_id) REFERENCES songs (song_id),
                                        FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
                                        FOREIGN KEY (start_time) REFERENCES time (start_time),
                                        FOREIGN KEY (user_id) REFERENCES users (user_id),
                                        UNIQUE (start_time, user_id, session_id));
""")                                                 

user_table_create = ("""
CREATE TYPE levels AS ENUM ('free', 'paid');
CREATE TYPE genders AS ENUM ('M', 'F');
CREATE TABLE IF NOT EXISTS users (user_id int NOT NULL,
                                    first_name varchar,
                                    last_name varchar,
                                    gender genders,
                                    level levels,
                                    PRIMARY KEY (user_id));
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (song_id varchar NOT NULL,
                                    title varchar,
                                    artist_id varchar,
                                    year int,
                                    duration float,
                                    PRIMARY KEY (song_id));
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (artist_id varchar NOT NULL,
                                    name varchar,
                                    location varchar,
                                    latitude real,
                                    longitude real,
                                    PRIMARY KEY (artist_id));
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (start_time timestamp NOT NULL,
                                    hour int,
                                    day int,
                                    week int,
                                    month int,
                                    year int,
                                    weekday int,
                                    PRIMARY KEY (start_time));
""")


# INSERT RECORDS
songplay_table_insert = ("""
INSERT INTO songplays (
    songplay_id, 
    start_time, 
    user_id, 
    level, 
    song_id, 
    artist_id, 
    session_id, 
    location, 
    user_agent) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
ON CONFLICT (songplay_id) DO NOTHING;
""")

user_table_insert = ("""
INSERT INTO users (
    user_id, 
    first_name, 
    last_name, 
    gender, 
    level) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) 
DO UPDATE
    SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (
    song_id, 
    title, 
    artist_id, 
    year, 
    duration) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (
    artist_id, 
    name, 
    location, 
    latitude, 
    longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = ("""
INSERT INTO time (
    start_time, 
    hour, 
    day, 
    week, 
    month, 
    year, 
    weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING;
""")


# FIND SONGS
song_select = ("""
SELECT 
    s.song_id, 
    s.artist_id 
FROM songs s 
JOIN artists a 
    ON s.artist_id = a.artist_id 
WHERE s.title = %s 
    AND a.name = %s 
    AND s.duration = %s;
""")


# QUERY LISTS
create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]