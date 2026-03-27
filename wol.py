import socket
import struct
import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    """Load WOL configuration from config.json."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file {CONFIG_FILE} not found.")

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def create_magic_packet(mac_address):
    """Create the Wake-on-LAN magic packet."""
    # Remove any separators from the MAC address
    mac = mac_address.replace(':', '').replace('-', '').replace('.', '')

    if len(mac) != 12:
        raise ValueError("Invalid MAC address format.")

    # Magic packet is 6 bytes of 0xFF followed by 16 repetitions of the target MAC address
    data = b'FF' * 6 + (mac.encode('ascii') * 16)

    # Convert hex string to bytes
    send_data = b''
    for i in range(0, len(data), 2):
        send_data = send_data + struct.pack('B', int(data[i: i + 2], 16))

    return send_data

def wake_on_lan():
    """Send a Wake-on-LAN packet using settings from config.json."""
    config = load_config()
    mac_address = config.get('mac_address')
    broadcast_ip = config.get('broadcast_ip', '255.255.255.255')
    port = config.get('port', 9)

    if not mac_address:
         raise ValueError("MAC address is missing from configuration.")

    magic_packet = create_magic_packet(mac_address)

    # Send UDP packet to broadcast address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (broadcast_ip, port))

    return {"status": "success", "message": f"WOL packet sent to {mac_address} at {broadcast_ip}:{port}"}

if __name__ == "__main__":
    try:
        result = wake_on_lan()
        print(result["message"])
    except Exception as e:
        print(f"Error: {e}")
