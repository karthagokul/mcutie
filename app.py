# app.py

from flask import Flask, render_template, request
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# MQTT client setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="backend")

def on_connect(mqttc, obj, flags, reason_code, properties):
    print("Connected with result code "+str(reason_code))
    client.subscribe(MQTT_TOPIC)

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.payload))
    # Emit message to WebSocket
    socketio.emit('mqtt_message', msg.payload.decode())

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    global MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
    MQTT_BROKER = request.form['broker']
    MQTT_PORT = int(request.form['port'])
    MQTT_TOPIC = request.form['topic']
    MQTT_USERNAME = request.form['username']
    MQTT_PASSWORD = request.form['password']

    # Connect to MQTT broker
    client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start MQTT loop in a separate thread
    client.loop_start()

    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=20001,debug=True)
