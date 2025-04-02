from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

from db import create_db_connection, view_latest_readings

POLL_INTERVAL = 5

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'secret!'

@app.route("/")
def index():
    return render_template('index.html')

def background_thread():
    while True:
      socketio.sleep(POLL_INTERVAL)
      data = view_latest_readings(create_db_connection, 3)
      print(data)
      socketio.emit("update_data", {"data": data},)

if __name__ == "__main__":
  socketio.start_background_task(target=background_thread)
  socketio.run(app, debug=True)
