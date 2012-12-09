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
    return 'Status goes here'

@app.route('/j/')
def index_json():
    return jsonify(machines=[])

def get_index_data():
    pass

@app.route('/grab/<int:id>', methods=['GET', 'POST'])
def grab_machine(id):
    pass

@app.route('/ungrab/<int:id>', methods=['GET', 'POST'])
def ungrab_machine(id):
    pass

if __name__ == '__main__':
    app.run(debug=True)
