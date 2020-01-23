import os
import sqlite3
from os.path import join, getsize
import face_recognition
import json
import click

@click.command()
@click.option('--year', default=2004, help='Year to Scan')
def main(year):
    conn = sqlite3.connect('fr_data_{}'.format(year))
    sql_files = """
    CREATE TABLE IF NOT EXISTS files (
        oid INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        path TEXT NOT NULL
    );
    """

    sql_faces = """
    CREATE TABLE IF NOT EXISTS faces (
        oid INTEGER PRIMARY KEY,
        file_oid TEXT NOT NULL,
        locations TEXT NOT NULL
    );
    """
    conn.execute(sql_files)
    conn.execute(sql_faces)
    cur = conn.cursor()

    total, skipped, processed = 0, 0, 0
    for root, dirs, files in os.walk('/Volumes/OSXternal/Picture Archive/{}'.format(year)):
        print(root, "consumes", end=" ")
        print(sum(getsize(join(root, name)) for name in files), end=" ")
        print("bytes in", len(files), "non-directory files")

        for file in files:
            total += 1
            if total % 5 == 0:
                print('total: {}, skipped: {}, processed: {}'.format(total, skipped, processed))
                conn.commit()

            if '.jpg' not in file.lower():
                skipped += 1
                continue
            
            processed += 1

            cur.execute('INSERT INTO files(filename, path) VALUES(?, ?)', (file, root))
            file_to_recog = face_recognition.api.load_image_file(os.path.join(root, file), mode='RGB')
            locs = face_recognition.api.face_locations(file_to_recog)

            cur.execute(
                'INSERT INTO faces(file_oid, locations) VALUES (?, ?)',
                (cur.lastrowid, json.dumps(locs))
            )

if __name__ == "__main__":
    main()