#!/usr/bin/python
# coding: utf-8

# Scenario 02 | Encrypted communication | Server side PoC

import opcua
import random
import time
import os

# Get the directory of the current script and set certificate and key paths
script_dir = os.path.dirname(os.path.abspath(__file__))
server_cert = os.path.join(script_dir, "../../certs/server/server_cert.pem")
server_key = os.path.join(script_dir, "../../certs/server/server_key.pem")

def generate_random_values():
    wind_direction = random.choice(["North", "South", "East", "West"])
    rotation_speed = random.randrange(1, 100, 5)
    wind_speed = random.randrange(1, 100, 5)
    electricity_production = wind_speed > 0 and rotation_speed > 0
    return electricity_production, wind_direction, rotation_speed, wind_speed

# Create a server instance
s = opcua.Server()
s.set_server_name("Chiphering_OPCUA_Server")
s.set_endpoint("opc.tcp://0.0.0.0:4840/PoC")
s.set_security_policy([opcua.ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt]) # type: ignore
s.load_certificate(server_cert)
s.load_private_key(server_key)

# Register the OPC-UA namespace
idx = s.register_namespace("Scenario02")
# start the OPC UA server (no tags at this point)
s.start()
objects = s.get_objects_node()

# First wind turbine
turbine1 = objects.add_object(idx, "Wind_Turbine_1")

# Add variables for Wind_Turbine_1
turbine1var1 = turbine1.add_variable(idx, "ElectricityProduction", True)
turbine1var1.set_writable(writable=True)

turbine1var2 = turbine1.add_variable(idx, "WindDirection", "West")
turbine1var2.set_writable(writable=True)

turbine1var3 = turbine1.add_variable(idx, "RotationSpeed", 0)
turbine1var3.set_writable(writable=True)

turbine1var4 = turbine1.add_variable(idx, "WindSpeed", 0)
turbine1var4.set_writable(writable=True)

# Second wind turbine
turbine2 = objects.add_object(idx, "Wind_Turbine_2")

# Add variables for Wind_Turbine_2
turbine2var1 = turbine2.add_variable(idx, "ElectricityProduction", True)
turbine2var1.set_writable(writable=True)

turbine2var2 = turbine2.add_variable(idx, "WindDirection", "South")
turbine2var2.set_writable(writable=True)

turbine2var3 = turbine2.add_variable(idx, "RotationSpeed", 0)
turbine2var3.set_writable(writable=True)

turbine2var4 = turbine2.add_variable(idx, "WindSpeed", 0)
turbine2var4.set_writable(writable=True)

# Update the values on the server
while True:
    # Generate random values for Wind_Turbine_1
    turbine1_electricity_production, turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed = generate_random_values()

    # Generate random values for Wind_Turbine_2
    turbine2_electricity_production, turbine2_wind_direction, turbine2_rotation_speed, turbine2_wind_speed = generate_random_values()

    # Set the values on the server for Wind_Turbine_1
    turbine1.get_child(["2:ElectricityProduction"]).set_value(turbine1_electricity_production)
    turbine1.get_child(["2:WindDirection"]).set_value(turbine1_wind_direction)
    turbine1.get_child(["2:RotationSpeed"]).set_value(turbine1_rotation_speed)
    turbine1.get_child(["2:WindSpeed"]).set_value(turbine1_wind_speed)

    # Set the values on the server for Wind_Turbine_2
    turbine2.get_child(["2:ElectricityProduction"]).set_value(turbine2_electricity_production)
    turbine2.get_child(["2:WindDirection"]).set_value(turbine2_wind_direction)
    turbine2.get_child(["2:RotationSpeed"]).set_value(turbine2_rotation_speed)
    turbine2.get_child(["2:WindSpeed"]).set_value(turbine2_wind_speed)

    # Wait for some time before updating again
    time.sleep(5)
