from flask import Flask, request, jsonify

# Create the Flask application
app = Flask(__name__)

# Dictionary that maps units to their category
# This helps ensure users only convert within the same category (e.g., length → length)
UNIT_CATEGORIES = {
    "km": "length",
    "mi": "length",
    "kg": "weight",
    "lb": "weight",
    "c": "temperature",
    "f": "temperature",
}

# Aliases allow users to type units in different formats
# and they will be converted into the standard internal unit names
UNIT_ALIASES = {
    # Length aliases
    "kilometer": "km",
    "kilometers": "km",
    "kms": "km",
    "km": "km",
    "mile": "mi",
    "miles": "mi",
    "mi": "mi",

    # Weight aliases
    "kilogram": "kg",
    "kilograms": "kg",
    "kgs": "kg",
    "kg": "kg",
    "pound": "lb",
    "pounds": "lb",
    "lbs": "lb",
    "lb": "lb",

    # Temperature aliases
    "c": "c",
    "°c": "c",
    "celsius": "c",
    "centigrade": "c",

    "f": "f",
    "°f": "f",
    "fahrenheit": "f",
}

# Standard format for returning JSON error responses
def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code


# Normalize user input units (remove spaces, lowercase, convert aliases)
def normalize_unit(u):
    if not isinstance(u, str):
        raise ValueError("Unit must be a string.")
    u = u.strip().lower()
    return UNIT_ALIASES.get(u, u)  # Convert alias or return unchanged


# Function that performs actual unit conversion
def convert_value(value, from_unit, to_unit):

    # If both units are the same, no conversion needed
    if from_unit == to_unit:
        return value

    # Length conversions
    if from_unit == "km" and to_unit == "mi":
        return value * 0.621371
    if from_unit == "mi" and to_unit == "km":
        return value / 0.621371

    # Weight conversions
    if from_unit == "kg" and to_unit == "lb":
        return value * 2.20462
    if from_unit == "lb" and to_unit == "kg":
        return value / 2.20462

    # Temperature conversions
    if from_unit == "c" and to_unit == "f":
        return value * 9/5 + 32
    if from_unit == "f" and to_unit == "c":
        return (value - 32) * 5/9

    # If no valid conversion was found
    raise ValueError("Unsupported conversion.")


# Root endpoint (basic welcome message)
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Unit Converter API"})


# Help endpoint that lists supported units
@app.route("/help", methods=["GET"])
def help():
    return jsonify({
        "supported_units": {
            "length": ["km", "mi"],
            "weight": ["kg", "lb"],
            "temperature": ["C", "F"]
        }
    })


# Main conversion endpoint
@app.route("/convert", methods=["POST"])
def convert():

    # Check if request contains valid JSON
    if not request.is_json:
        return error_response("Content-Type must be application/json")

    # Parse the JSON body
    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid JSON.")

    # Check if required fields are provided
    for f in ("value", "from_unit", "to_unit"):
        if f not in data:
            return error_response(f"Missing field: {f}")

    # Validate that value is numeric
    try:
        value = float(data["value"])
    except:
        return error_response("Value must be numeric.")

    # Normalize units (remove spaces, lowercase, map aliases)
    from_unit = normalize_unit(data["from_unit"])
    to_unit = normalize_unit(data["to_unit"])

    # Check if both units are supported
    if from_unit not in UNIT_CATEGORIES or to_unit not in UNIT_CATEGORIES:
        return error_response("Unknown unit.")

    # Ensure both units belong to the same category
    if UNIT_CATEGORIES[from_unit] != UNIT_CATEGORIES[to_unit]:
        return error_response("Invalid conversion between categories.")

    # Length and weight cannot be negative
    if UNIT_CATEGORIES[from_unit] in ("length", "weight") and value < 0:
        return error_response("Negative values not allowed for length/weight.")

    # Try performing the conversion
    try:
        result = convert_value(value, from_unit, to_unit)
    except Exception as e:
        return error_response(str(e))

    # Successful conversion response
    return jsonify({
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "converted_value": result
    })


# Run the Flask application (debug mode enabled)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
