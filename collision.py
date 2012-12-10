from flask import Flask, jsonify, g
from contextlib import closing
import sqlite3

app = Flask(__name__)
DATABASE = 'db/sqlite_db.txt'

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('db/schema.sql') as f:
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
@app.route('/machines')
def index():
    state = fetch_index_data()
    return 'Status goes here'

@app.route('/j/')
def index_json():
    state = fetch_index_data()
    return jsonify(machines=str(state))

def fetch_index_data():
    """Builds and returns the current State"""
    return State()

@app.route('/did/<event_name>/on/<hostname>/in/<branch_name>/for/<username>',
           methods=['POST', 'GET'])
def write_step(event_name, hostname, branch_name, username):
    """Writes a named step on a machine"""
    host = verify_hostname(hostname)
    user = verify_user(username)
    branch = verify_branch(branch_name)

    event = verify_event(event_name)

    if hostname and event and branch and user:
        return jsonify(status='OK',
                       host=host,
                       event=event,
                       branch=branch,
                       user=user,
                       id='step_id')
    else:
        return jsonify(status='FAIL')

@app.route('/users/')
def show_users():
    return ""

@app.route('/user/<username>')
def show_single_user(username):
    user = verify_user(username, shouldCreate=False)

    if user:
        return jsonify(status="OK")
    else:
        return jsonify(status="BAD")

@app.route('/branches/')
def show_branches():
    return ""

@app.route('/branch/<branchname>')
def show_single_branch(branchname):
    branch = verify_branch(branchname)

    if branch:
        return jsonify(status="OK")
    else:
        return jsonify(status="BAD")

def verify_event(event_name):
    return True

def verify_hostname(hostname):
    return True

def verify_branch(branch_name):
    return True

def verify_user(username, shouldCreate=True):
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
