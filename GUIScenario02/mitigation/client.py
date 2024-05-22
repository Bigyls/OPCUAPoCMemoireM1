#!/usr/bin/python
# coding: utf-8

import opcua
import time
import os
import signal

class MitigationClient():
    def __init__(self):
        # Get the directory of the current script and set certificate and key paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.client_cert = os.path.join(self.script_dir, "../../certs/client/client_cert.pem")
        self.client_key = os.path.join(self.script_dir, "../../certs/client/client_key.pem")

        # Create OPC-UA client
        self.client = opcua.Client("opc.tcp://localhost:4840/PoC")
        self.user, self.password = 'admin', 'admin'
        self.client.set_user(self.user)
        self.client.set_password(self.password)
        self.client.set_security_string(f"Basic256Sha256,SignAndEncrypt,{self.client_cert},{self.client_key}")
        self.client.connect()
        self.client.open_secure_channel(True)
        self.root = self.client.get_root_node()
        self.objects = self.client.get_objects_node()
        self.set_connected_user(self.user)
        self.turbine1 = self.objects.get_child(["2:Turbines", "2:Wind_Turbine_1"])
        self.turbine2 = self.objects.get_child(["2:Turbines", "2:Wind_Turbine_2"])

    # Get the values from the server
    def get_node_value(self, node):
        return node.get_child(node.get_children()[0].get_browse_name()).get_value(), \
            node.get_child(node.get_children()[1].get_browse_name()).get_value(), \
            node.get_child(node.get_children()[2].get_browse_name()).get_value(), \
            node.get_child(node.get_children()[3].get_browse_name()).get_value(), \
            node.get_child(node.get_children()[4].get_browse_name()).get_value()

    def set_connected_user(self, user):
        user_management = self.objects.get_child(["2:Administration", "2:UserManagement"])
        user = user_management.get_children()[0].set_value(user)

    def run(self):
        while True:
            # Clear the terminal
            os.system('/usr/bin/clear')
            print(f"User: {self.user}\n")

            # Get values for Wind_Turbine_1
            turbine1_electricity_production, turbine1_maintenance_mode, turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed = self.get_node_value(self.turbine1)
            print("Wind Turbine 1")
            print("Electricity Production: ", turbine1_electricity_production)
            print("Maintenance Mode: ", turbine1_maintenance_mode)
            print("Wind Direction: ", turbine1_wind_direction)
            print("Rotation Speed: ", turbine1_rotation_speed)
            print("Wind Speed: ", turbine1_wind_speed)

            # Get values for Wind_Turbine_2
            turbine2_electricity_production, turbine2_maintenance_mode, turbine2_wind_direction, turbine2_rotation_speed, turbine2_wind_speed = self.get_node_value(self.turbine2)
            print("\n")
            print("Wind Turbine 2")
            print("Electricity Production: ", turbine2_electricity_production)
            print("Maintenance Mode: ", turbine2_maintenance_mode)
            print("Wind Direction: ", turbine2_wind_direction)
            print("Rotation Speed: ", turbine2_rotation_speed)
            print("Wind Speed: ", turbine2_wind_speed)

            # Get the values from the server
            time.sleep(2)

if __name__ == "__main__":
    client = MitigationClient()
    client.run()
