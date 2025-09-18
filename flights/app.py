from flasgger import Swagger
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import get_random_int
import pyroscope

pyroscope.configure(
  application_name = "flights",
  server_address   = "https://profiles-prod-002.grafana.net",
  basic_auth_username = "1370456",
  basic_auth_password = "<REDACTED>",
  sample_rate         = 100, # default is 100
  detect_subprocesses = False, # detect subprocesses started by the main process; default is False
  oncpu               = True, # report cpu time only; default is True
  gil_only            = True, # only include traces for threads that are holding on to the Global Interpreter Lock; default is True
  enable_logging      = True, # does enable logging facility; default is False
    tags                = {
        "env": "dev",
        "namespace":"pov-sim",
        "service_name": "flights",
    }
)

app = Flask(__name__)
Swagger(app)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    """Health endpoint
    ---
    responses:
      200:
        description: Returns healthy
    """
    return jsonify({"status": "healthy"}), 200

@app.route("/", methods=['GET'])
def home():
    """No-op home endpoint
    ---
    responses:
      200:
        description: Returns ok
    """
    return jsonify({"message": "ok"}), 200

@app.route("/flights/<airline>", methods=["GET"])
def get_flights(airline):
    """Get flights endpoint. Optionally, set raise to trigger an exception.
    ---
    parameters:
      - name: airline
        in: path
        type: string
        enum: ["AA", "UA", "DL"]
        required: true
      - name: raise
        in: query
        type: str
        enum: ["500"]
        required: false
    responses:
      200:
        description: Returns a list of flights for the selected airline
    """
    status_code = request.args.get("raise")
    if status_code:
      raise Exception(f"Encountered {status_code} error") # pylint: disable=broad-exception-raised
    random_int = get_random_int(100, 999)
    return jsonify({airline: [random_int]}), 200

@app.route("/flight", methods=["POST"])
def book_flight():
    """Book flights endpoint. Optionally, set raise to trigger an exception.
    ---
    parameters:
      - name: passenger_name
        in: query
        type: string
        enum: ["John Doe", "Jane Doe"]
        required: true
      - name: flight_num
        in: query
        type: string
        enum: ["101", "202", "303", "404", "505", "606"]
        required: true
      - name: raise
        in: query
        type: str
        enum: ["500"]
        required: false
    responses:
      200:
        description: Booked a flight for the selected passenger and flight_num
    """
    status_code = request.args.get("raise")
    if status_code:
      raise Exception(f"Encountered {status_code} error") # pylint: disable=broad-exception-raised
    passenger_name = request.args.get("passenger_name")
    flight_num = request.args.get("flight_num")
    booking_id = get_random_int(100, 999)
    return jsonify({"passenger_name": passenger_name, "flight_num": flight_num, "booking_id": booking_id}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
