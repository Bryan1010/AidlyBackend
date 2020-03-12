import os
from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

app.config['MONGO_URI'] = os.environ.get('DB')
print(os.environ.get('DB'))

if(__name__ == "__main__"):
    app.run(debug=True)