#!/usr/bin/python
# coding: utf-8

import opcua
import random
import time
import os

from opcua.server.user_manager import UserManager

class MitigationServer():
    def __init__(self):
        # Get the directory of the current script and set certificate and key paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.server_cert = os.path.join(self.script_dir, "../../certs/server/server_cert.pem")
        self.server_key = os.path.join(self.script_dir, "../../certs/server/server_key.pem")

        # User management with credentials
        self.users_db =  {'admin': 'admin', 'guest': 'guest'}

        # Create a server instance
        self.server = opcua.Server()
        self.server.set_server_name("PoC OPCUA Server")
        self.server.set_endpoint("opc.tcp://0.0.0.0:4840/PoC")
        self.server.set_security_policy([opcua.ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt]) # type: ignore
        self.server.load_certificate(self.server_cert)
        self.server.load_private_key(self.server_key)
        self.server.set_security_IDs(["Username"])
        self.server.user_manager.set_user_manager(self.user_manager) # type: ignore

        # Register the OPC-UA namespace
        self.idx = self.server.register_namespace("Scenario01")
        # start the OPC UA server (no tags at this point)
        self.objects = self.server.get_objects_node()

        self.administration_folder = self.objects.add_folder(self.idx, "Administration")
        self.user = self.administration_folder.add_object(self.idx, "UserManagement")
        self.uservar1 = self.user.add_variable(self.idx, "ConnectedUser", "")
        self.uservar1.set_writable(writable=True)

    def user_manager(self, isession, username, password):
        isession.user = UserManager.User
        return username in self.users_db and password == self.users_db[username]

    # Generate random values for the wind turbines
    def generate_random_values(self):
        wind_direction = random.choice(["North", "South", "East", "West"])
        rotation_speed = random.randrange(30, 40, 1)
        wind_speed = random.randrange(80, 120, 5)
        return wind_direction, rotation_speed, wind_speed

    def define_variables_and_methods(self, turbine1, turbine2, maintenance_methods_folder, electricity_methods_folder):
        # Add variables and methods for Wind_Turbine_1
        self.add_variables_and_methods(turbine1, self.idx)
        # Add variables and methods for Wind_Turbine_2
        self.add_variables_and_methods(turbine2, self.idx)

        # Add methods in folders
        self.add_method(maintenance_methods_folder, "enable_maintenance_mode", self.enable_maintenance_mode, [])
        self.add_method(maintenance_methods_folder, "disable_maintenance_mode", self.disable_maintenance_mode, [])
        self.add_method(electricity_methods_folder, "enable_electricity_production", self.enable_electricity_production, [])
        self.add_method(electricity_methods_folder, "disable_electricity_production", self.disable_electricity_production, [])

    def add_variables_and_methods(self, turbine, idx):
        # Add variables for the turbine
        for var_name in ["ElectricityProduction", "MaintenanceMode", "WindDirection", "RotationSpeed", "WindSpeed"]:
            var = turbine.add_variable(idx, var_name, False) if var_name != "MaintenanceMode" else turbine.add_variable(idx, var_name, True)
            var.set_writable(writable=True)

    def add_method(self, folder, method_name, method_func, input_arguments):
        folder.add_method(self.idx, method_name, method_func, input_arguments)

    # OPC UA methods
    # Enable maintenance mode
    @opcua.uamethod
    def enable_maintenance_mode(self, parent):
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_1", "2:MaintenanceMode"]).set_value(True)
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_2", "2:MaintenanceMode"]).set_value(True)
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(False)
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(False)
        return True

    # Disable maintenance mode
    @opcua.uamethod
    def disable_maintenance_mode(self, parent):
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_1", "2:MaintenanceMode"]).set_value(False)
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_2", "2:MaintenanceMode"]).set_value(False)
        return True

    # Enable electricity production
    @opcua.uamethod
    def enable_electricity_production(self, parent):
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_1", "2:MaintenanceMode"]).set_value(False)
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_2", "2:MaintenanceMode"]).set_value(False)
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(True)
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(True)
        return True

    # Disable electricity production
    @opcua.uamethod
    def disable_electricity_production(self, parent):
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_1", "2:ElectricityProduction"]).set_value(False)
        self.server.get_objects_node().get_child(["2:Turbines", "2:Wind_Turbine_2", "2:ElectricityProduction"]).set_value(False)
        return True

    def update_turbine_values(self, turbine1, turbine2):
        # Generate random values for Wind_Turbine_1
        turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed = self.generate_random_values()
        # Generate random values for Wind_Turbine_2
        turbine2_wind_direction, turbine2_rotation_speed, turbine2_wind_speed = self.generate_random_values()

        # Set the values on the server for Wind_Turbine_1
        self.set_turbine_values(turbine1, turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed)
        # Set the values on the server for Wind_Turbine_2
        self.set_turbine_values(turbine2, turbine2_wind_direction, turbine2_rotation_speed, turbine2_wind_speed)

    def set_turbine_values(self, turbine, wind_direction, rotation_speed, wind_speed):
        turbine.get_child(["2:WindDirection"]).set_value(wind_direction)
        turbine.get_child(["2:RotationSpeed"]).set_value(rotation_speed)
        turbine.get_child(["2:WindSpeed"]).set_value(wind_speed)

    def run(self):
        # Start the OPC UA server
        self.server.start()

        # Create folders for the turbines and methods
        turbine_folders = self.objects.add_folder(self.idx, "Turbines")
        methods_folder = self.objects.add_folder(self.idx, "Methods")
        maintenance_methods_folder = methods_folder.add_folder(self.idx, "Maintenance")
        electricity_methods_folder = methods_folder.add_folder(self.idx, "Electricity")

        # First wind turbine
        turbine1 = turbine_folders.add_object(self.idx, "Wind_Turbine_1")
        # Second wind turbine
        turbine2 = turbine_folders.add_object(self.idx, "Wind_Turbine_2")

        # Define variables for turbines and add methods
        self.define_variables_and_methods(turbine1, turbine2, maintenance_methods_folder, electricity_methods_folder)

        # Update the values on the server
        while True:
            turbine1_electricity_production = turbine1.get_child(["2:ElectricityProduction"]).get_value()
            turbine1_maintenance_mode = turbine1.get_child(["2:MaintenanceMode"]).get_value()
            turbine2_electricity_production = turbine2.get_child(["2:ElectricityProduction"]).get_value()
            turbine2_maintenance_mode = turbine2.get_child(["2:MaintenanceMode"]).get_value()

            # Generate random values for Wind_Turbine_1
            turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed = self.generate_random_values()

            # Generate random values for Wind_Turbine_2
            turbine2_wind_direction, turbine2_rotation_speed, turbine2_wind_speed = self.generate_random_values()

            # Set the values on the server for Wind_Turbine_1
            turbine1.get_child(["2:WindDirection"]).set_value(turbine1_wind_direction)
            turbine1.get_child(["2:RotationSpeed"]).set_value(turbine1_rotation_speed)
            turbine1.get_child(["2:WindSpeed"]).set_value(turbine1_wind_speed)

            # Set the values on the server for Wind_Turbine_2
            turbine2.get_child(["2:WindDirection"]).set_value(turbine2_wind_direction)
            turbine2.get_child(["2:RotationSpeed"]).set_value(turbine2_rotation_speed)
            turbine2.get_child(["2:WindSpeed"]).set_value(turbine2_wind_speed)

            if not turbine1_electricity_production and not turbine2_electricity_production or turbine1_maintenance_mode or turbine2_maintenance_mode:

                # stop the turbines if they are in maintenance mode or electricity production is disabled
                turbine1.get_child(["2:RotationSpeed"]).set_value(0)
                turbine2.get_child(["2:RotationSpeed"]).set_value(0)

            time.sleep(1)

# Main
if __name__ == "__main__":
    server = MitigationServer()
    server.run()
