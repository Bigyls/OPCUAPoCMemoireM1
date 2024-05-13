#!/usr/bin/python
# coding: utf-8

## Communication sans chiffrement

# Creation of an OPCUA server and simulation of tags 
import opcua 
import random 
import time

# Create a server instance
s = opcua.Server() 
s.set_server_name("Poc_OPCUA_Server") 
s.set_endpoint("opc.tcp://0.0.0.0:4840")
 
# Register the OPC-UA namespace 
idx = s.register_namespace("http://localhost:4840") 
# start the OPC UA server (no tags at this point) 
s.start() 
objects = s.get_objects_node() 

# Firt wind turbine 
# Define a Wind turbine object with some tags 
turbine1 = objects.add_object(idx, "Wind_Turbine_1") 
# Add a Roation tag with a value and boolean 
turbine1var1 = turbine1.add_variable(idx, "ElectricityProduction", True) 
turbine1var1.set_writable(writable=True) 
# Add a Wind direction tag with a value and string 
turbine1var2 = turbine1.add_variable(idx, "WindDirection", "West") 
turbine1var2.set_writable(writable=True) 
# Add a Windspeed tag with a value and range 
turbine1var3 = turbine1.add_variable(idx, "RotationSpeed", 0) 
turbine1var3.set_writable(writable=True) 
# Add a Wind speed tag with a value and string 
turbine1var4 = turbine1.add_variable(idx, "WindSpeed", 0) 
turbine1var4.set_writable(writable=True) 

# Second wind turbine 
# Define a Wind turbine object with some tags 
turbine2 = objects.add_object(idx, "Wind_Turbine_2") 
# Add a Roation tag with a value and boolean 
turbine2var1 = turbine2.add_variable(idx, "ElectricityProduction", True) 
turbine2var1.set_writable(writable=True) 
# Add a Wind direction tag with a value and string 
turbine2var2 = turbine2.add_variable(idx, "WindDirection", "South") 
turbine2var2.set_writable(writable=True) 
# Add a Windspeed tag with a value and range 
turbine2var3 = turbine2.add_variable(idx, "RotationSpeed", 0) 
turbine2var3.set_writable(writable=True) 
# Add a Wind speed tag with a value and string 
turbine2var4 = turbine2.add_variable(idx, "WindSpeed", 0) 
turbine2var4.set_writable(writable=True)

# Create some simulated data
# Create OPC-UA client
client = opcua.Client("opc.tcp://localhost:4840")
# Connect to the server
client.connect()
# Get the root node
root = client.get_root_node()
# Get the objects node
objects = client.get_objects_node()
# Get the Wind_Turbine_1 node
turbine1 = objects.get_child(["2:Wind_Turbine_1"])
# Get the Wind_Turbine_2 node
turbine2 = objects.get_child(["2:Wind_Turbine_2"])

# Update the values on the server
while True:
    # Generate random values for the tags
    wind_direction = random.choice(["North", "South", "East", "West"])
    rotation_speed = random.randint(0, 100)
    wind_speed = random.randint(0, 10)
    if(wind_speed > 0 and rotation_speed > 0):
        electricity_production = True
    else:
        electricity_production = False

    # Set the values on the server
    turbine1.get_child(["2:ElectricityProduction"]).set_value(electricity_production)
    turbine1.get_child(["2:WindDirection"]).set_value(wind_direction)
    turbine1.get_child(["2:RotationSpeed"]).set_value(rotation_speed)
    turbine1.get_child(["2:WindSpeed"]).set_value(wind_speed)

    turbine2.get_child(["2:ElectricityProduction"]).set_value(electricity_production)
    turbine2.get_child(["2:WindDirection"]).set_value(wind_direction)
    turbine2.get_child(["2:RotationSpeed"]).set_value(rotation_speed)
    turbine2.get_child(["2:WindSpeed"]).set_value(wind_speed)

    # Wait for some time before updating again
    time.sleep(5)