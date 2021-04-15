from flask import Flask #Flask framework imported
from threading import Thread #threading imported

app = Flask('') #sets up Flask as a function

@app.route('/') 
def home(): 
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
