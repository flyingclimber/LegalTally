'''  
  LegalTally -- LegalTally is python flask based application that takes 
  user input and sends it to a ProLite Led sign over serial
 
  Copyright (C) 2012, Tomasz Finc <tomasz@gmail.com>
  
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import sqlite3, serial, time, ProLite
from flask import Flask, g, redirect, url_for, render_template, flash, request
from contextlib import closing

app = Flask(__name__)
app.config.from_pyfile('default_settings.py')

### DB section ###
def init_db():
    '''Create the initial db'''
    with closing(connect_db()) as db_:
        with app.open_resource('schema.sql') as f:
            db_.cursor().executescript(f.read())
        db_.commit()

def connect_db():
    '''Open the configured DB'''
    return sqlite3.connect(app.config['DATABASE'])

### End DB Section ###

### Web Code ###
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
    cur = g.db.execute('select text, count, id from tally order by id')
    entries = [dict(text=row[0], count=row[1], id=row[2]) 
            for row in cur.fetchall()]
    colors = ProLite.ProLite.colors
    formats = ProLite.ProLite.formats
    functions = ProLite.ProLite.functions
    return render_template('show_tally.html', entries=entries, colors=colors, 
                                                formats=formats, functions=functions)

@app.route('/increment/<key>', methods=['GET'])
def increment(key):
    '''Increment the counter for the specified token'''
    if key is None:
        flash('Invalid key')
    else:
        g.db.execute('update tally set count = count + 1 where id = \'%s\'' 
                % key)
        g.db.commit()
        flash('Tally Updated')

    update_sign()
    return redirect(url_for('show_tally'))

@app.route('/reset')
def reset():
    '''Reset the counter and update the sign'''
    g.db.execute('update tally set count = 0')
    g.db.commit()
    flash('Tally Reset')
    update_sign()
    return redirect(url_for('show_tally'))

@app.route('/delete/<key>', methods=['GET'])
def delete(key):
    '''Delete the given count'''
    if key is None:
        flash('Invalid key')
    else:
        g.db.execute('delete from tally where id = \'%s\'' % key)
        g.db.commit()
        flash('Deleted key')
        update_sign()
        return redirect(url_for('show_tally'))

@app.route('/new_metric', methods=['POST'])
def new_metric():
    '''Add a new metric to the db'''
    g.db.execute('insert into tally (text, count) values (?, ?)', 
            [request.form['metric'], 0])
    g.db.commit()
    update_sign()
    flash('Added new tally')
    return redirect(url_for('show_tally'))

@app.route('/refersh')
def refresh():
    '''Refresh the display on the sign'''
    update_sign()
    return redirect(url_for('show_tally'))

### End Web Code ###

### Serial Code ###
def update_sign(message=None):
    '''
        Take the incoming message and send it to the sign over serial. 
        If no message it set then lookup the strings in the db
    '''
    unit = 'ProLite.UNIT'
    page = 'ProLite.PAGE_1'
    color = 'LIME'
    speed = 'SPEED_1'

    if message == None:
        message = ''
        cur = g.db.execute('select text, count from tally order by id')
        entries = [dict(text=row[0], count=row[1]) for row in cur.fetchall()]
        divider = " / "
        for entry in entries:
            message = "%s %s %s : %s" % (message, divider, 
                    entry['text'], entry['count'])
    try:
        message = "%s%s%s%s %s" % (unit, page, color, speed, message)
        flash("Sending %s" % message)
        ser = serial.Serial(app.config['DEVICE'], app.config['BAUD_RATE'])
        ser.write('%s\r\n' % ProLite.UNIT)
        time.sleep(1)
        ser.write('%s / \r\n' % message)
        ser.close()
    except IOError:
        flash('Couldn\'t update sign')

#### End Serial Code ###

if __name__ == '__main__':
    app.run(host='0.0.0.0')
