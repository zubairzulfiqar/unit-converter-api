# Unit Converter API  
**Author:** Zubair Zulfiqar  
**Email:** zubairzulfiqar96@gmail.com  

A lightweight Flask API for converting units of length, weight, and temperature.

## Running the project

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Access the API at:  
`http://localhost:5000`

## Endpoints

### `POST /convert`
Convert values between supported units.

Example:
```json
{
  "value": 10,
  "from_unit": "km",
  "to_unit": "mi"
}
```

### `GET /help`
Lists supported conversions.

## Supported Units
- **Length:** km, mi  
- **Weight:** kg, lb  
- **Temperature:** C, F  

Negative values are allowed only for temperatures.
