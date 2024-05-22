#!/usr/bin/python
# coding: utf-8

# Scenario 02 | Mitigation | Server side PoC

import opcua
import random
import time
import os

from opcua.server.user_manager import UserManager

# Get the directory of the current script and set certificate and key paths
script_dir = os.path.dirname(os.path.abspath(__file__))
server_cert = os.path.join(script_dir, "../../certs/server/server_cert.pem")
server_key = os.path.join(script_dir, "../../certs/server/server_key.pem")

# Generate random values for the wind turbines
def generate_random_values():
    wind_direction = random.choice(["North", "South", "East", "West"])
    rotation_speed = random.randrange(30, 40, 1)
    wind_speed = random.randrange(80, 120, 5)
    return wind_direction, rotation_speed, wind_speed

# OPC UA methods
# Enable maintenance mode
@opcua.uamethod
def enable_maintenance_mode(parent):
    objects.get_child(["2:Turbines", "2:Wind_Turbine_1", "2:MaintenanceMode"]).set_value(True)
    objects.get_child(["2:Turbines", "2:Wind_Turbine_2", "2:MaintenanceMode"]).set_value(True)
    objects.get_child(["2:Turbines", "2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(False)
    objects.get_child(["2:Turbines", "2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(False)
    return True

# Disable maintenance mode
@opcua.uamethod
def disable_maintenance_mode(parent):
    objects.get_child(["2:Turbines", "2:Wind_Turbine_1", "2:MaintenanceMode"]).set_value(False)
    objects.get_child(["2:Turbines", "2:Wind_Turbine_2", "2:MaintenanceMode"]).set_value(False)
    objects.get_child(["2:Turbines", "2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(True)
    objects.get_child(["2:Turbines", "2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(True)
    return True

# Enable electricity production
@opcua.uamethod
def enable_electricity_production(parent):
    objects.get_child(["2:Turbines", "2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(True)
    objects.get_child(["2:Turbines", "2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(True)
    return True

# Disable electricity production
@opcua.uamethod
def disable_electricity_production(parent):
    objects.get_child(["2:Turbines", "2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(False)
    objects.get_child(["2:Turbines", "2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(False)
    return True

# User management with credentials
users_db =  {'admin': 'admin', 'guest': 'guest'}

def user_manager(isession, username, password):
    isession.user = UserManager.User
    return username in users_db and password == users_db[username]

# Main
if __name__ == "__main__":
    # Create a server instance
    server = opcua.Server()
    server.set_server_name("PoC OPCUA Server")
    server.set_endpoint("opc.tcp://0.0.0.0:4840/PoC")
    server.set_security_policy([opcua.ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt]) # type: ignore
    server.load_certificate(server_cert)
    server.load_private_key(server_key)
    server.set_security_IDs(["Username"])
    server.user_manager.set_user_manager(user_manager) # type: ignore

    # Register the OPC-UA namespace
    idx = server.register_namespace("Scenario02")
    # start the OPC UA server (no tags at this point)
    server.start()
    objects = server.get_objects_node()

    # Create a folder for the administration
    administration_folder = objects.add_folder(idx, "Administration")

    # User Node
    user = administration_folder.add_object(idx, "UserManagement")
    uservar1 = user.add_variable(idx, "ConnectedUser", "")
    uservar1.set_writable(writable=True)

    # Create a folder for the turbines
    turbine_folders = objects.add_folder(idx, "Turbines")

    # First wind turbine
    turbine1 = turbine_folders.add_object(idx, "Wind_Turbine_1")

    # Add variables for Wind_Turbine_1
    turbine1var1 = turbine1.add_variable(idx, "ElectricityProduction", False)
    turbine1var1.set_writable(writable=True)

    turbine1var1 = turbine1.add_variable(idx, "MaintenanceMode", True)
    turbine1var1.set_writable(writable=True)

    turbine1var2 = turbine1.add_variable(idx, "WindDirection", "North")
    turbine1var2.set_writable(writable=True)

    turbine1var3 = turbine1.add_variable(idx, "RotationSpeed", 0)
    turbine1var3.set_writable(writable=True)

    turbine1var4 = turbine1.add_variable(idx, "WindSpeed", 0)
    turbine1var4.set_writable(writable=True)

    # Second wind turbine
    turbine2 = turbine_folders.add_object(idx, "Wind_Turbine_2")

    # Add variables for Wind_Turbine_2
    turbine2var1 = turbine2.add_variable(idx, "ElectricityProduction", False)
    turbine2var1.set_writable(writable=True)

    turbine2var2 = turbine2.add_variable(idx, "MaintenanceMode", True)
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
    enable_maintenance_mode_method = maintenance_methods_folder.add_method(idx, "enable_maintenance_mode", enable_maintenance_mode, [], [opcua.ua.VariantType.Boolean]) # type: ignore
    disable_maintenance_mode_method = maintenance_methods_folder.add_method(idx, "disable_maintenance_mode", disable_maintenance_mode, [], [opcua.ua.VariantType.Boolean]) # type: ignore
    enable_electricity_production_method = electricity_methods_folder.add_method(idx, "enable_electricity_production", enable_electricity_production, [], [opcua.ua.VariantType.Boolean]) # type: ignore
    disable_electricity_production_method = electricity_methods_folder.add_method(idx, "disable_electricity_production", disable_electricity_production, [], [opcua.ua.VariantType.Boolean]) # type: ignore

    # Update the values on the server
    while True:
        turbine1_electricity_production = turbine1.get_child(["2:ElectricityProduction"]).get_value()
        turbine1_maintenance_mode = turbine1.get_child(["2:MaintenanceMode"]).get_value()
        turbine2_electricity_production = turbine2.get_child(["2:ElectricityProduction"]).get_value()
        turbine2_maintenance_mode = turbine2.get_child(["2:MaintenanceMode"]).get_value()

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

        # Check if the turbines are in production mode and not in maintenance mode
        if not turbine1_electricity_production and not turbine2_electricity_production or turbine1_maintenance_mode or turbine2_maintenance_mode:

            # stop the turbines if they are in maintenance mode or electricity production is disabled
            turbine1.get_child(["2:RotationSpeed"]).set_value(0)
            turbine2.get_child(["2:RotationSpeed"]).set_value(0)
            time.sleep(5)
