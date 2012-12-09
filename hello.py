from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/status')
def machine_status():
    pass

@app.route('/grab/<int:id>', methods=['GET', 'POST'])
def grab_machine(id):
    pass

@app.route('/ungrab/<int:id>', methods=['GET', 'POST'])
def ungrab_machine(id):
    pass

if __name__ == '__main__':
    app.run(debug=True)
