#!/usr/bin/python
# coding: utf-8

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
    rotation_speed = random.randrange(30, 40, 1)
    wind_speed = random.randrange(80, 120, 5)
    return wind_direction, rotation_speed, wind_speed

# OPC UA methods
# Enable maintenance mode
@opcua.uamethod
def EnableMaintenanceMode(parent):
    objects.get_child(["2:Wind_Turbine_1", "2:MaintenanceMode"]).set_value(True)
    objects.get_child(["2:Wind_Turbine_2", "2:MaintenanceMode"]).set_value(True)
    objects.get_child(["2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(False)
    objects.get_child(["2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(False)
    return True

# Disable maintenance mode
@opcua.uamethod
def DisableMaintenanceMode(parent):
    objects.get_child(["2:Wind_Turbine_1", "2:MaintenanceMode"]).set_value(False)
    objects.get_child(["2:Wind_Turbine_2", "2:MaintenanceMode"]).set_value(False)
    objects.get_child(["2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(True)
    objects.get_child(["2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(True)
    return True

# Enable electricity production
@opcua.uamethod
def EnableElectricityProduction(parent):
    objects.get_child(["2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(True)
    objects.get_child(["2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(True)
    return True

# Disable electricity production
@opcua.uamethod
def DisableElectricityProduction(parent):
    objects.get_child(["2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(False)
    objects.get_child(["2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(False)
    return True

if __name__ == "__main__":
    # Create a server instance
    s = opcua.Server()
    s.set_server_name("PoC OPCUA Server")
    s.set_endpoint("opc.tcp://0.0.0.0:4840/PoC")
    s.set_security_policy([opcua.ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt]) # type: ignore
    s.load_certificate(server_cert)
    s.load_private_key(server_key)
    # Register the OPC-UA namespace
    idx = s.register_namespace("Scenario01")
    # start the OPC UA server (no tags at this point)
    s.start()
    objects = s.get_objects_node()

    # First wind turbine
    turbine1 = objects.add_object(idx, "Wind_Turbine_1")

    # Add variables for Wind_Turbine_1
    turbine1var1 = turbine1.add_variable(idx, "ElectricityProduction", True)
    turbine1var1.set_writable(writable=True)

    turbine1var1 = turbine1.add_variable(idx, "MaintenanceMode", False)
    turbine1var1.set_writable(writable=True)

    turbine1var2 = turbine1.add_variable(idx, "WindDirection", "North")
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

    turbine2var2 = turbine2.add_variable(idx, "MaintenanceMode", False)
    turbine2var2.set_writable(writable=True)

    turbine2var2 = turbine2.add_variable(idx, "WindDirection", "North")
    turbine2var2.set_writable(writable=True)

    turbine2var3 = turbine2.add_variable(idx, "RotationSpeed", 0)
    turbine2var3.set_writable(writable=True)

    turbine2var4 = turbine2.add_variable(idx, "WindSpeed", 0)
    turbine2var4.set_writable(writable=True)

    # Create folders method
    methodsfolder = objects.add_folder(idx, "Methods")
    maintenance_methods_folder = methodsfolder.add_folder(idx, "Maintenance")
    electricity_methods_folder = methodsfolder.add_folder(idx, "Electricity")

    # Add methods in folders
    enable_maintenance_mode_method = maintenance_methods_folder.add_method(idx, "EnableMaintenanceMode", EnableMaintenanceMode, [], [opcua.ua.VariantType.Boolean]) # type: ignore
    disable_maintenance_mode_method = maintenance_methods_folder.add_method(idx, "DisableMaintenanceMode", DisableMaintenanceMode, [], [opcua.ua.VariantType.Boolean]) # type: ignore
    enable_electricity_production_method = electricity_methods_folder.add_method(idx, "EnableElectricityProduction", EnableElectricityProduction, [], [opcua.ua.VariantType.Boolean]) # type: ignore
    disable_electricity_production_method = electricity_methods_folder.add_method(idx, "DisableElectricityProduction", DisableElectricityProduction, [], [opcua.ua.VariantType.Boolean]) # type: ignore

    # Update the values on the server
    while True:
        turbine1_electricity_production = turbine1.get_child(["2:ElectricityProduction"]).get_value()
        turbine1_maintenance_mode = turbine1.get_child(["2:MaintenanceMode"]).get_value()
        turbine2_electricity_production = turbine2.get_child(["2:ElectricityProduction"]).get_value()
        turbine2_maintenance_mode = turbine2.get_child(["2:MaintenanceMode"]).get_value()

        # Check if the turbines are in production mode and not in maintenance mode
        if turbine1_electricity_production and not turbine1_maintenance_mode and turbine2_electricity_production and not turbine2_maintenance_mode:
            # Generate random values for Wind_Turbine_1
            turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed = generate_random_values()

            # Generate random values for Wind_Turbine_2
            turbine2_wind_direction, turbine2_rotation_speed, turbine2_wind_speed = generate_random_values()

            # Set the values on the server for Wind_Turbine_1
            turbine1.get_child(["2:WindDirection"]).set_value(turbine1_wind_direction)
            turbine1.get_child(["2:RotationSpeed"]).set_value(turbine1_rotation_speed)
            turbine1.get_child(["2:WindSpeed"]).set_value(turbine1_wind_speed)

            # Set the values on the server for Wind_Turbine_2
            turbine2.get_child(["2:WindDirection"]).set_value(turbine2_wind_direction)
            turbine2.get_child(["2:RotationSpeed"]).set_value(turbine2_rotation_speed)
            turbine2.get_child(["2:WindSpeed"]).set_value(turbine2_wind_speed)

            # Wait for some time before updating again
            time.sleep(5)

        else:
            # stop the turbines if they are in maintenance mode or electricity production is disabled
            turbine1.get_child(["2:WindDirection"]).set_value(0)
            turbine1.get_child(["2:RotationSpeed"]).set_value(0)
            turbine1.get_child(["2:WindSpeed"]).set_value(0)

            turbine2.get_child(["2:WindDirection"]).set_value(0)
            turbine2.get_child(["2:RotationSpeed"]).set_value(0)
            turbine2.get_child(["2:WindSpeed"]).set_value(0)
            time.sleep(5)
