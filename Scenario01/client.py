#!/usr/bin/python
# coding: utf-8

# Scenario 01 | No ciphering communication | Client side PoC

import opcua
import time

def get_node_value(node):
    return node.get_child(node.get_children()[0].get_browse_name()).get_value(), \
           node.get_child(node.get_children()[1].get_browse_name()).get_value(), \
           node.get_child(node.get_children()[2].get_browse_name()).get_value(), \
           node.get_child(node.get_children()[3].get_browse_name()).get_value()

# Create OPC-UA client
client = opcua.Client("opc.tcp://localhost:4841")

# Connect to the server
client.connect()

# Get the root node
root = client.get_root_node()

# Get the objects node
objects = client.get_objects_node()

# Get Wind_Turbine_1 node
turbine1 = objects.get_child(["2:Wind_Turbine_1"])

# Get Wind_Turbine_2 node
turbine2 = objects.get_child(["2:Wind_Turbine_2"])

while True:


    # Get values for Wind_Turbine_1
    turbine1_electricity_production, turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed = get_node_value(turbine1)
    print("Wind Turbine 1")
    print("Electricity Production: ", turbine1_electricity_production)
    print("Wind Direction: ", turbine1_wind_direction)
    print("Rotation Speed: ", turbine1_rotation_speed)
    print("Wind Speed: ", turbine1_wind_speed)

    # Get values for Wind_Turbine_2
    turbine2_electricity_production, turbine2_wind_direction, turbine2_rotation_speed, turbine2_wind_speed = get_node_value(turbine2)
    print("Wind Turbine 2")
    print("Electricity Production: ", turbine2_electricity_production)
    print("Wind Direction: ", turbine2_wind_direction)
    print("Rotation Speed: ", turbine2_rotation_speed)
    print("Wind Speed: ", turbine2_wind_speed)

    # Get the values from the server
    time.sleep(5)
