from flask import Flask, jsonify
from contextlib import closing

app = Flask(__name__)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    state = get_index_data()
    return 'Status goes here'

@app.route('/j/')
def index_json():
    state = get_index_data()
    return jsonify(machines=state.machines)

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

class Machine:
    """Defines a merge machine"""
    def __init__(self, name):
        self.name = 'hostname'
        self.id = None
        self.last_event = None

class State():
    """Current state of the merge machines"""
    def __init__(self):
        self.machines = self.fetch_machines()

    def fetch_machines(self):
        return [
            "merge",
            "merge2",
            "merge3"
            ]


if __name__ == '__main__':
    app.run(debug=True)
