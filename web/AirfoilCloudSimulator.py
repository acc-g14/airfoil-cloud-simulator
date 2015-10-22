#imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
import json

#config
DATABASE = 'databases/addDB.db'
DEBUG = True #remember to disable!
SECRET_KEY = 'development key' #replace with some other techniques to keep the client-side sessions secure?
USERNAME = 'admin' #develop registration functionalities and store in a salted hashed DB?
PASSWORD = 'default' # -\\-

app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('FLASKR_SETTINGS', silent = True)
"""
That way someone can set an environment variable called FLASKR_SETTINGS to specify a config file to be loaded which will then override the default values. The silent switch just tells Flask to not complain if no such environment key is set.
"""

# Login view - login options
@app.route('/')
def show_login():
    return render_template('main_login.html', error=None)


# Main view - the user dashboard
@app.route('/dashboard')
def show_dashboard():
    return render_template('dashboard.html')


# Logging in - fix to setup user DB and management
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Username not valid'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Password not valid'
        else:
            session['logged_in'] = True
            flash('You are now logged in')
            return redirect(url_for('jobs'))
    return render_template('main_login.html', error=error)

# Logging out - fix to adhere to updated user management
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('show_login'))

@app.route('/service_status')
def service_status():
    return render_template('service_status.html')

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    existing_jobs = ["job1", "job2", "job3"]
    return render_template('jobs.html', existing_jobs=map(json.dumps, existing_jobs))

@app.route('/new_job')
def new_job():
    existing_jobs = ["job1", "job2", "job3"]
    return render_template('new_job.html', existing_jobs=existing_jobs)

if __name__ == '__main__':
    app.run()
