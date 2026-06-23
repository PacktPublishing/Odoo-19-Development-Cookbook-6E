import requests
import json

# Odoo server URL
odoo_url = "http://localhost:8069/api/legacy/create_data"

# Payload includes credentials and the room data to create
payload = {
    "params": {
        "db": "odoo-test",
        "username": "admin",
        "password": "admin",
        "data": {
            "name": "Serpent CS",
            "room_no": "501",
            "description": "Serpent Consulting Services Pvt Ltd."
        }
    }
}

# Send POST request to the Odoo controller
response = requests.post(
    odoo_url,
    json=payload,
    headers={'Content-Type': 'application/json'}
)

# Print the response from Odoo
print("Response Status:", response.status_code)
print("Response JSON:", json.dumps(response.json(), indent=4))