from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Gravitational acceleration values (m/s^2) for different planets
PLANET_GRAVITY = {
    "Earth": 9.8,
    "Moon": 1.62,
    "Mars": 3.71,
    "Jupiter": 24.79,
    "Venus": 8.87,
    "Saturn": 10.44,
    "Mercury": 3.7,
    "Neptune": 11.15
}

@app.route('/')
def home():
    # Serve the HTML file directly
    return send_file('index.html')

@app.route('/planets')
def get_planets():
    return jsonify(PLANET_GRAVITY)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Check required fields
        if 'mass' not in data:
            return jsonify({"error": "Missing 'mass' field"}), 400
        if 'planet' not in data:
            return jsonify({"error": "Missing 'planet' field"}), 400
        
        # Validate inputs
        try:
            mass = float(data['mass'])
        except (ValueError, TypeError):
            return jsonify({"error": "Mass must be a valid number"}), 400
        
        planet = data['planet']
        if planet not in PLANET_GRAVITY:
            return jsonify({"error": f"Unknown planet: {planet}"}), 400
        
        if mass < 0:
            return jsonify({"error": "Mass cannot be negative"}), 400
        if mass == 0:
            return jsonify({"error": "Mass cannot be zero"}), 400

        # Get planet's gravity and calculate force using F = ma
        acceleration = PLANET_GRAVITY[planet]
        force = round(mass * acceleration, 2)
        
        return jsonify({
            "mass": mass,
            "planet": planet,
            "acceleration": acceleration,
            "force": force,
            "formula": "F = ma"
        })
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)