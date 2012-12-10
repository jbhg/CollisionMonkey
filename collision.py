from flask import Flask, jsonify, g
from contextlib import closing
import sqlite3

app = Flask(__name__)
DATABASE = 'db/sqlite_db.txt'

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    state = get_index_data()
    return 'Status goes here'

@app.route('/j/')
def index_json():
    state = get_index_data()
    return jsonify(machines=str(state))

def get_index_data():
    """Builds and returns the current State"""
    return State()

@app.route('/did/<step_name>/on/<hostname>/in/<branch>',
           methods=['POST', 'GET'])
def write_step(step_name, hostname, branch):
    """Writes a named step on a machine"""
    if verify_hostname(hostname) and verify_step(step_name):
        return jsonify(status='OK',
                       hostname=hostname,
                       step=step_name,
                       branch=branch,
                       id='step_id')

def verify_step(step_name):
    return True

def verify_hostname(hostname):
    return True

def verify_branch(hostname):
    return True

## Class stubs

class Event:
    """An event is anything that happens on a machine, e.g. grab or SUCCESS_*"""
    def __init__(self):
        self.id = 1
        self.timestamp = 1
        self.name = None

class Branch:
    """Grouping class for an entire merge"""
    def __init__(self):
        self.branchname = 'svn name'
        self.owner = 'ldap'
        self.events = []

    def __str__(self):
        return '{{ branchname={self.branchname}, owner={self.owner}, events={self.events} }}'.format(self=self)
    def __repr__(self):
        return self.__str__()

class Machine:
    """Defines a merge machine"""
    def __init__(self, name):
        self.name = name
        self.id = None
        self.last_event = None

    def __str__(self):
        return '{{ name={self.name}, id={self.id}, last_event={self.last_event} }}'.format(self=self)
    def __repr__(self):
        return self.__str__()

class State():
    """Current state of the merge machines"""
    def __init__(self):
        self.machines = self.fetch_machines()

    def fetch_machines(self):
        return [
            Machine("merge"),
            Machine("merge2"),
            Machine("merge3")
            ]

    def __str__(self):
        return str(self.machines)
    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    app.run(debug=True)
