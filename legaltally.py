# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

### DB section ###
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

### Web Code ###
@app.route('/')
def show_tally():
    return render_template('show_tally.html')

@app.route('/plus_one/<increment>')
def plus_one(increment):
    if increment == 'approved':
        g.db.execute('update tally set approved = approved + 1 where id = 2') ## BROKEN
    if increment == 'denied':
        g.db.execute('update tally set denied = denied + 1 where id = 2') ## BROKEN
    d.db.commit()
    flash('Tally Updated')
    return redirect(url_for('show_tally'))

if __name__ == '__main__':
    app.run()


