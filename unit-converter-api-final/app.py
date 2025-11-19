"""
Unit Converter API
Author: Zubair Zulfiqar
Email: zubairzulfiqar96@gmail.com
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

UNIT_CATEGORIES = {
    "km": "length",
    "mi": "length",
    "kg": "weight",
    "lb": "weight",
    "c": "temperature",
    "f": "temperature",
}

UNIT_ALIASES = {
    "kilometer": "km",
    "kilometers": "km",
    "kms": "km",
    "km": "km",
    "mile": "mi",
    "miles": "mi",
    "mi": "mi",

    "kilogram": "kg",
    "kilograms": "kg",
    "kgs": "kg",
    "kg": "kg",
    "pound": "lb",
    "pounds": "lb",
    "lbs": "lb",
    "lb": "lb",

    "c": "c",
    "°c": "c",
    "celsius": "c",
    "centigrade": "c",

    "f": "f",
    "°f": "f",
    "fahrenheit": "f",
}


def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code


def normalize_unit(u):
    if not isinstance(u, str):
        raise ValueError("Unit must be a string.")
    u = u.strip().lower()
    return UNIT_ALIASES.get(u, u)


def convert_value(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    if from_unit == "km" and to_unit == "mi":
        return value * 0.621371
    if from_unit == "mi" and to_unit == "km":
        return value / 0.621371

    if from_unit == "kg" and to_unit == "lb":
        return value * 2.20462
    if from_unit == "lb" and to_unit == "kg":
        return value / 2.20462

    if from_unit == "c" and to_unit == "f":
        return value * 9/5 + 32
    if from_unit == "f" and to_unit == "c":
        return (value - 32) * 5/9

    raise ValueError("Unsupported conversion.")


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Unit Converter API"})


@app.route("/help", methods=["GET"])
def help():
    return jsonify({
        "supported_units": {
            "length": ["km", "mi"],
            "weight": ["kg", "lb"],
            "temperature": ["C", "F"]
        }
    })


@app.route("/convert", methods=["POST"])
def convert():
    if not request.is_json:
        return error_response("Content-Type must be application/json")

    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid JSON.")

    for f in ("value", "from_unit", "to_unit"):
        if f not in data:
            return error_response(f"Missing field: {f}")

    try:
        value = float(data["value"])
    except:
        return error_response("Value must be numeric.")

    from_unit = normalize_unit(data["from_unit"])
    to_unit = normalize_unit(data["to_unit"])

    if from_unit not in UNIT_CATEGORIES or to_unit not in UNIT_CATEGORIES:
        return error_response("Unknown unit.")

    if UNIT_CATEGORIES[from_unit] != UNIT_CATEGORIES[to_unit]:
        return error_response("Invalid conversion between categories.")

    if UNIT_CATEGORIES[from_unit] in ("length", "weight") and value < 0:
        return error_response("Negative values not allowed for length/weight.")

    try:
        result = convert_value(value, from_unit, to_unit)
    except Exception as e:
        return error_response(str(e))

    return jsonify({
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "converted_value": result
    })


if __name__ == "__main__":
    app.run(debug=True)
