import requests
import json

# Odoo server URL (adjust port/domain as needed)
odoo_url = "http://localhost:1900/api/legacy/order"

# Data to send (example order)
payload = {"params":{
    "name": "Serpent CS",
    "room_no": "301",
    "description": "Serpent Consulting Services Pvt Ltd."}
}

# Send POST request
# Sends data as JSON
response = requests.post(
    odoo_url,
    json=payload,          
    headers={'Content-Type': 'application/json'}
)

# Print the response from Odoo
print("Response Status:", response.status_code)
print("Response JSON:", json.dumps(response.json(), indent=4))
