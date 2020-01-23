from flask import render_template, send_file
from app.landing import landing_bp
import urllib.parse
import sqlite3
import os.path

@landing_bp.route('/', methods=['GET'])
def home():
    text = 'This is the landing route!'
    return render_template('landing.html', content=text)

@landing_bp.route('/info', methods=['GET'])
def info():
    text = 'This is the info route! Here is a kitten:'
    return render_template('info.html', content=text)

@landing_bp.route('/info', methods=['PUT'])
def update_info():
    return 'You have made a put request!'

@landing_bp.route('/photo_page/<file_oid>', methods=['GET'])
def get_photo_path(file_oid: int):
    return render_template('photo.html', file_oid=file_oid)

@landing_bp.route('/actual_photo/<file_oid>', methods=['GET'])
def get_photo(file_oid: int):
    conn = sqlite3.connect('../fr/master_db.db')
    cur = conn.cursor()

    query = """
        SELECT
            filename,
            path,
            locations
        FROM
            files JOIN faces ON files.oid = faces.file_oid
        WHERE
            files.oid = "{}";
        """.format(file_oid)

    print(query)

    cur.execute(query)

    path = cur.fetchone()
    x = send_file(os.path.join(path[1], path[0]))
    return x
    