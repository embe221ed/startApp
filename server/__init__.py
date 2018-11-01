from flask import Flask, render_template, request, jsonify
from flask import send_from_directory, session, url_for, redirect
from flask_session import Session
import json
import os
import sys
import psycopg2

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
SESSION_TYPE = 'filesystem'
SECRET_KEY = b'secret-key'
SESSION_FILE_DIR = '/var/www/startapp.com/flask_session/'
app.config.from_object(__name__)
sess = Session()
sess.init_app(app)

###############################################################################
# PATHS 
###############################################################################

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if not session.get('logged_in', False):
        return redirect(url_for('loginPage'))
    return render_template('index.html')

@app.route("/loginPage")
def loginPage():
    if not session.get('logged_in', False):
        return render_template('index.html')
    return redirect('/')

###############################################################################
# REST API
###############################################################################

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return ('', 200)

@app.route("/login", methods=['POST', 'GET'])
def login():
    data = request.data
    data = json.loads(data)
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("SELECT login, password FROM site_user WHERE login = '{}'"
        .format(data['userName']))
    result = cur.fetchall()
    username = result[0][0]
    password = result[0][1]
    if password == data['password']:
        session['logged_in'] = True
        return json.dumps({"status": "success"})
    else:
        return json.dumps({"status": "failure"})

@app.route("/addComment", methods=['POST'])
def add_comment():
    data = request.data
    data = json.loads(data)
    return json.dumps(data)

if __name__ == "__main__":
    app.debug = True
    app.run()
