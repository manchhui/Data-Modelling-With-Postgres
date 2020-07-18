import os
import glob
import psycopg2
import pandas as pd
from sql_queries import create_table_queries, drop_table_queries, songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert, song_select

def process_song_file(cur, filepath):
    """
    - Takes in the song dataset filepath from the "process_data" function
    - Reads in song JSON files and extracts the required data from each song to populated the song and artist tables
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(df[['song_id','title','artist_id','year','duration']].values)
    for song in song_data:
        cur.execute(song_table_insert, song)
    
    # insert artist record
    artist_data = list(df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values)
    for artist in artist_data:
        cur.execute(artist_table_insert, artist)


def process_log_file(cur, filepath):
    """
    - Takes in the log dataset filepath from the "process_data" function
    - Reads in log JSON files and extracts/transforms the required data to populated the time, user and songplay tables
    """
    # open log file
    df = pd.read_json(filepath, lines=True) 

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = list(zip(t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday))
    column_labels = ('time_stamp', 'hour', 'day', 'weekofyear', 'month', 'year', 'weekday') 
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (index, pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Takes in the upper level filepath and exacts all the filepaths for each JSON file.
    - Then passes the filepaths for each JSON file to the either function "process_song_file" or "process_log_file", which is called by the main function.
    - This function will also prints to screen the number of files it found and the number of files it has processed.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Sets up the connection to the database.
    - Calls the process data twice, first to process song files and then the log files.
    - Then closes the connection to the database.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()