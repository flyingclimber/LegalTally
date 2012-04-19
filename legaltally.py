'''Legal Tally -  A simple controller for counting take down requests and
    displaying them on an LED SIGN'''
import sqlite3, serial, time
from flask import Flask, g, redirect, url_for, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/tmp/legaltally.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DEVICE = '/dev/ttyUSB0'
BAUD_RATE = 9600

app = Flask(__name__)
app.config.from_object(__name__)

### DB section ###
def init_db():
    '''Create the initial db'''
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    '''Open a db connection'''
    return sqlite3.connect(app.config['DATABASE'])

### end db section ###

### web code ###
@app.before_request
def before_request():
    '''Open a db connection before the web view is served'''
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    '''Close the db handle after the web request is over'''
    if exception:
        print exception
    g.db.close()

@app.errorhandler(404)
def not_found(error):
    '''404 handler'''
    if error:
        print error
    return render_template('error.html'), 404

@app.route('/')
def show_tally():
    '''Show the default tally web view'''
    cur = g.db.execute('select received, denied from tally')
    entries = [dict(received=row[0], denied=row[1]) for row in cur.fetchall()]
    return render_template('show_tally.html', entries=entries)

@app.route('/plus_one/<increment>', methods=['GET'])
def plus_one(increment):
    '''Increment either the received or denied counter and update the sign'''
    if increment == 'received':
        g.db.execute('update tally set received = received + 1 where id = 1')
    if increment == 'denied':
        g.db.execute('update tally set denied = denied + 1 where id = 1') 
    g.db.commit()

    flash('Tally Updated')
    cur = g.db.execute('select received, denied from tally')
    entries = [dict(received=row[0], denied=row[1]) for row in cur.fetchall()]
    update_sign("Approved: %s Denied: %s" % 
            (entries[0]['received'], entries[0]['denied']))
    return redirect(url_for('show_tally'))

@app.route('/reset')
def reset():
    '''Reset the counter and update the sign'''
    g.db.execute('update tally set received = 0, denied = 0 where id = 1')
    g.db.commit()
    flash('Tally Reset')
    update_sign("Approved: 0 Denied: 0")
    return redirect(url_for('show_tally'))


### End Web Code ###

### Serial Code ###
def update_sign(message):
    '''Take the incoming message and send it to the sign'''
    try:
        ser = serial.Serial(DEVICE, BAUD_RATE)
        ser.write('<ID01>\r\n')
        time.sleep(1)
        ser.write('<ID01><PA><CI><FX> %s / \r\n' % message)
        ser.close()
    except IOError:
        flash('Couldn\'t update sign')

#### End Serial Code ###

if __name__ == '__main__':
    app.run(host='0.0.0.0')
