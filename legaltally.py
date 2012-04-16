# all the imports
import sqlite3, serial, time
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/legaltally.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DEVICE = '/tmp/ttyUSB0'
BAUD_RATE = 9600

app = Flask(__name__)
app.config.from_object(__name__)

### DB section ###
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

### End DB Section ###

### Web Code ###
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.route('/')
def show_tally():
    cur = g.db.execute('select approved, denied from tally')
    entries = [dict(approved=row[0], denied=row[1]) for row in cur.fetchall()]
    return render_template('show_tally.html', entries=entries)

@app.route('/plus_one/<increment>', methods=['GET'])
def plus_one(increment):
    if increment == 'approved':
        g.db.execute('update tally set approved = approved + 1 where id = 1')
    if increment == 'denied':
        g.db.execute('update tally set denied = denied + 1 where id = 1') 
    g.db.commit()

    flash('Tally Updated')
    cur = g.db.execute('select approved, denied from tally')
    entries = [dict(approved=row[0], denied=row[1]) for row in cur.fetchall()]
    update_sign("Approved: %s Denied: %s" % (entries[0]['approved'], entries[0]['denied']));
    return redirect(url_for('show_tally'))

### End Web Code ###

### Serial Code ###
def update_sign(message):
    ser = serial.Serial(DEVICE, BAUDRATE)
    ser.write('<ID01>\r\n')
    time.sleep(1)
    ser.write('<ID01><PA><FQ><CC> %s \r\n' % message)
    ser.close()

#### End Serial Code ###

if __name__ == '__main__':
    app.run(host='0.0.0.0')


