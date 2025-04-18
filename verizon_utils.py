import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verizon API credentials and URLs
VERIZON_API_KEY = os.getenv('VERIZON_API_KEY')
VERIZON_CLIENT_ID = os.getenv('VERIZON_CLIENT_ID')
VERIZON_CLIENT_SECRET = os.getenv('VERIZON_CLIENT_SECRET')
VERIZON_ACCOUNT = os.getenv('VERIZON_ACCOUNT')
VERIZON_SMS_ACCOUNT_NAME = os.getenv('VERIZON_SMS_ACCOUNT_NAME')
VERIZON_SANDBOX_URL = os.getenv('VERIZON_SANDBOX_URL', 'https://api.verizon.com')
VERIZON_DEVICES_ENDPOINT = '/api/m2m/v1/devices'
VERIZON_MESSAGE_ENDPOINT = '/api/m2m/v1/sms'

# Check if we should simulate Verizon API responses
SIMULATE_VERIZON = os.getenv('SIMULATE_VERIZON_SUCCESS', 'false').lower() == 'true'
print(f"Verizon simulation mode: {SIMULATE_VERIZON}")

def get_sample_devices():
    """
    Return sample devices for development/testing
    """
    print("Returning sample devices for demonstration")
    sample_devices = [
        {
            'id': '123456789',
            'name': 'Sample Device 1',
            'type': 'Smartphone',
            'status': 'Active'
        },
        {
            'id': '987654321',
            'name': 'Sample Device 2',
            'type': 'Tablet',
            'status': 'Active'
        },
        {
            'id': '555555555',
            'name': 'Sample Device 3',
            'type': 'IoT Device',
            'status': 'Inactive'
        }
    ]
    print(f"Sample devices: {json.dumps(sample_devices, indent=2)}")
    return sample_devices

def get_devices():
    """
    Get available devices through the Verizon API.
    
    Returns:
        list: List of device dictionaries with id and name
    """
    print("Getting devices...")
    
    # Use sample devices if simulation mode is enabled
    if SIMULATE_VERIZON:
        devices = get_sample_devices()
        print(f"Returning {len(devices)} simulated devices")
        return devices
    
    # Check if we have the required credentials
    if not all([VERIZON_API_KEY, VERIZON_CLIENT_ID, VERIZON_CLIENT_SECRET, VERIZON_ACCOUNT]):
        print("Error: Missing Verizon API credentials")
        return get_sample_devices()  # Fall back to sample devices
    
    # Make real API call to Verizon
    headers = {
        'Authorization': f'Bearer {VERIZON_API_KEY}',
        'Content-Type': 'application/json'
    }
    params = {
        'account': VERIZON_ACCOUNT
    }
    
    try:
        print(f"Making API call to {VERIZON_SANDBOX_URL}{VERIZON_DEVICES_ENDPOINT}")
        response = requests.get(
            f"{VERIZON_SANDBOX_URL}{VERIZON_DEVICES_ENDPOINT}",
            headers=headers,
            params=params,
            timeout=10  # Increase timeout
        )
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        devices = data.get('devices', [])
        
        # Format the devices for our application
        formatted_devices = []
        for device in devices:
            formatted_devices.append({
                'id': device.get('id', ''),
                'name': device.get('name', 'Unknown Device'),
                'type': device.get('type', 'Unknown'),
                'status': device.get('status', 'Unknown')
            })
        
        print(f"Successfully retrieved {len(formatted_devices)} devices from Verizon API")
        return formatted_devices
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Verizon API: {str(e)}")
        print("Falling back to sample devices")
        return get_sample_devices()

def send_message(device_id, message):
    """
    Send a message to a device through the Verizon API.
    
    Args:
        device_id (str): The ID of the device to send the message to
        message (str): The message to send
        
    Returns:
        dict: Response with success status and message
    """
    print(f"Sending message to device {device_id}")
    
    # Use simulation if enabled
    if SIMULATE_VERIZON:
        print(f"Simulating successful message send to device {device_id}")
        return {
            'success': True,
            'message': f"Successfully sent message to device {device_id} (SIMULATED)"
        }
    
    # Check if we have the required credentials
    if not all([VERIZON_API_KEY, VERIZON_CLIENT_ID, VERIZON_CLIENT_SECRET, VERIZON_ACCOUNT, VERIZON_SMS_ACCOUNT_NAME]):
        print("Error: Missing Verizon API credentials")
        return {
            'success': False,
            'message': "Failed to send message: Missing Verizon API credentials"
        }
    
    # Prepare the request
    headers = {
        'Authorization': f'Bearer {VERIZON_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'accountName': VERIZON_SMS_ACCOUNT_NAME,
        'deviceIds': [device_id],
        'message': message
    }
    
    try:
        print(f"Making API call to {VERIZON_SANDBOX_URL}{VERIZON_MESSAGE_ENDPOINT}")
        response = requests.post(
            f"{VERIZON_SANDBOX_URL}{VERIZON_MESSAGE_ENDPOINT}",
            headers=headers,
            json=payload,
            timeout=10  # Increase timeout
        )
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        
        print(f"Successfully sent message to device {device_id}")
        return {
            'success': True,
            'message': f"Successfully sent message to device {device_id}"
        }
        
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to send message: {str(e)}"
        print(error_message)
        return {
            'success': False,
            'message': error_message
        } 