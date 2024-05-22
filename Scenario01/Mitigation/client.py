#!/usr/bin/python
# coding: utf-8

# Scenario 01 | Migitation | Client side PoC

import opcua
import time
import os
import argparse
import platform

# Parse command line arguments to get the server IP address
parser = argparse.ArgumentParser(description="Client side PoC")
parser.add_argument("-i", "--ip", type=str, help="Server IP address")
args = parser.parse_args()

# Determine the operating system
OS = platform.system()

# Define a handler class for subscription events
class SubscriptionHandler(object):
    def __init__(self) -> None:
        self.values = []

    # Handle data change notifications
    def datachange_notification(self, node, val, data):
        # Match node IDs to their corresponding browsenames
        match(node.nodeid.Identifier):
            case 7:
                nodeBrowName = "WindTurbine2 Electricity Production"
            case 8:
                nodeBrowName = "WindTurbine2 Wind Direction"
            case 9:
                nodeBrowName = "WindTurbine2 Rotation Speed"
            case 10:
                nodeBrowName = "WindTurbine2 Wind Speed"

        # Delete the element with the same browsename
        self.values = [(name, value) for name, value in self.values if name != nodeBrowName]

        # Append the new value
        self.values.append((nodeBrowName, val))

        # Sort the values by their browsenames
        self.values.sort(key=lambda x: x[0])

        # Clear the console screen based on the operating system
        if(OS == "Windows"):
            os.system("cls")
        else:
            print("\033c", end="")

        # Print the updated values
        for nodeBrowName, val in self.values:
            print(f"Node: {nodeBrowName}\n Value: {val}\n")

        # Print Wind Turbine 1 details
        print("Wind Turbine 1")
        print("Electricity Production: ", turbine1_electricity_production)
        print("Wind Direction: ", turbine1_wind_direction)
        print("Rotation Speed: ", turbine1_rotation_speed)
        print("Wind Speed: ", turbine1_wind_speed)

# Function to get values of all child nodes of a given node
def get_node_value(node):
    return node.get_child(node.get_children()[0].get_browse_name()).get_value(), \
           node.get_child(node.get_children()[1].get_browse_name()).get_value(), \
           node.get_child(node.get_children()[2].get_browse_name()).get_value(), \
           node.get_child(node.get_children()[3].get_browse_name()).get_value()

# Get the directory of the current script and set certificate and key paths
script_dir = os.path.dirname(os.path.abspath(__file__))
client_cert = os.path.join(script_dir, "../../certs/client/client_cert.pem")
client_key = os.path.join(script_dir, "../../certs/client/client_key.pem")

# Create OPC-UA client
client = opcua.Client(f"opc.tcp://{args.ip}:4840/PoC")
client.set_security_string(f"Basic256Sha256,SignAndEncrypt,{client_cert},{client_key}")

# Connect to the server
client.connect()
client.open_secure_channel(True)

# Get the root node
root = client.get_root_node()

# Get the objects node
objects = client.get_objects_node()

# Get Wind_Turbine_1 node
turbine1 = objects.get_child(["2:Wind_Turbine_1"])

# Get Wind_Turbine_2 node
turbine2 = objects.get_child(["2:Wind_Turbine_2"])

# Create the subscription
handler = SubscriptionHandler()
sub = client.create_subscription(5000, handler)

# Subscribe to data changes for Wind_Turbine_2 variables
turbine2_handle_WindSpeed = sub.subscribe_data_change(turbine2.get_child(["2:WindSpeed"]))
turbine2_handle_WindDirection = sub.subscribe_data_change(turbine2.get_child(["2:WindDirection"]))
turbine2_handle_Rotation_Speed = sub.subscribe_data_change(turbine2.get_child(["2:RotationSpeed"]))
turbine2_handle_ElectricityProduction = sub.subscribe_data_change(turbine2.get_child(["2:ElectricityProduction"]))

try:
    while True:
        # Get values for Wind_Turbine_1
        turbine1_electricity_production, turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed = get_node_value(turbine1)
        time.sleep(4.8)

except KeyboardInterrupt:
    # Disconnect client on keyboard interrupt
    client.disconnect()
finally:
    # Unsubscribe and delete the subscription
    sub.unsubscribe(turbine2_handle_WindSpeed)
    sub.unsubscribe(turbine2_handle_WindDirection)
    sub.unsubscribe(turbine2_handle_Rotation_Speed)
    sub.unsubscribe(turbine2_handle_ElectricityProduction)
    sub.delete()
