#!/usr/bin/python
# coding: utf-8

# Scenario 03 | Encrypted PubSub | Client side PoC

import opcua
import time
import os

class SubscriptionHandler(object):
    def __init__(self) -> None:
        self.values = []
    
    def datachange_notification(self, node, val, data):
        if (2 == node.nodeid.Identifier):
            nodeBrowName = "WindTurbine1 Electricity Production"
        elif (3 == node.nodeid.Identifier):
            nodeBrowName = "WindTurbine1 Wind Direction"
        elif (4 == node.nodeid.Identifier):
            nodeBrowName = "WindTurbine1 Rotation Speed"
        elif (5 == node.nodeid.Identifier):
            nodeBrowName = "WindTurbine1 Wind Speed"
        elif (7 == node.nodeid.Identifier):
            nodeBrowName = "WindTurbine2 Electricity Production"
        elif (8 == node.nodeid.Identifier):
            nodeBrowName = "WindTurbine2 Wind Direction"
        elif (9 == node.nodeid.Identifier):
            nodeBrowName = "WindTurbine2 Rotation Speed"
        elif (10 == node.nodeid.Identifier):
            nodeBrowName = "WindTurbine2 Wind Speed"
            
        # Delete the element with the same browsename
        self.values = [(name, value) for name, value in self.values if name != nodeBrowName]
            
        self.values.append((nodeBrowName, val))
        
        self.values.sort(key=lambda x: x[0])
            
        print("\033c",end="")
        
        for nodeBrowName, val in self.values:
            print(f"Node: {nodeBrowName}\n Value: {val}\n")

# Get the directory of the current script and set certificate and key paths
script_dir = os.path.dirname(os.path.abspath(__file__))
client_cert = os.path.join(script_dir, "../certs/client/client_cert.pem")
client_key = os.path.join(script_dir, "../certs/client/client_key.pem")

# Create OPC-UA client
client = opcua.Client("opc.tcp://localhost:4840/PoC")
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

# Creating the subscription
handler = SubscriptionHandler()
sub = client.create_subscription(500, handler)
turbine1_handle_WindSpeed = sub.subscribe_data_change(turbine1.get_child(["2:WindSpeed"]))
turbine1_handle_WindDirection = sub.subscribe_data_change(turbine1.get_child(["2:WindDirection"]))
turbine1_handle_Rotation_Speed = sub.subscribe_data_change(turbine1.get_child(["2:RotationSpeed"]))
turbine1_handle_ElectricityProduction = sub.subscribe_data_change(turbine1.get_child(["2:ElectricityProduction"]))

turbine2_handle_WindSpeed = sub.subscribe_data_change(turbine2.get_child(["2:WindSpeed"]))
turbine2_handle_WindDirection = sub.subscribe_data_change(turbine2.get_child(["2:WindDirection"]))
turbine2_handle_Rotation_Speed = sub.subscribe_data_change(turbine2.get_child(["2:RotationSpeed"]))
turbine2_handle_ElectricityProduction = sub.subscribe_data_change(turbine2.get_child(["2:ElectricityProduction"]))

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    sub.unsubscribe(turbine1_handle_WindSpeed)
    sub.unsubscribe(turbine1_handle_WindDirection)
    sub.unsubscribe(turbine1_handle_Rotation_Speed)
    sub.unsubscribe(turbine1_handle_ElectricityProduction)
    sub.unsubscribe(turbine2_handle_WindSpeed)
    sub.unsubscribe(turbine2_handle_WindDirection)
    sub.unsubscribe(turbine2_handle_Rotation_Speed)
    sub.unsubscribe(turbine2_handle_ElectricityProduction)
    sub.delete()
