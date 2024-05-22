
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

import threading
import time

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk,ttk, font, Button, PhotoImage, Label, StringVar

from data.gauge import Gauge
from data.roundedcanva import RoundedCanvas
from exploitation.server import ExploitationServer
from exploitation.client import ExploitationClient

from mitigation.server import MitigationServer
from mitigation.client import MitigationClient


class GUI():
	def __init__(self, mode):
		self.mode = mode

	def run_exploitation_server(self):
		self.server = ExploitationServer()
		self.server.run()

	def run_exploitation_client(self):
		self.client = ExploitationClient()
		self.client.run()

	def run_mitigation_server(self):
		self.server = MitigationServer()
		self.server.run()

	def run_mitigation_client(self):
		self.client = MitigationClient()
		self.client.run()

	def run_gui(self):

		OUTPUT_PATH = Path(__file__).parent
		ASSETS_PATH = OUTPUT_PATH / Path(r"../assets")

		def relative_to_assets(path: str) -> Path:
			return ASSETS_PATH / Path(path)

		window = Tk()

		window.geometry("1144x647")
		window.configure(bg = "#0085BA")

		myfont24 = font.Font(family='Roboto Bold', size=24 * -1, weight="bold")
		myfont16 = font.Font(family='Roboto Bold', size=16 * -1)
		myboldfont16 = font.Font(family='Roboto Bold', size=16 * -1, weight="bold")

		canvas = RoundedCanvas(
			window,
			bg = "#0085BA",
			height = 647,
			width = 1144,
			bd = 0,
			highlightthickness = 0,
			relief = "ridge"
		)

		canvas.place(x = 0, y = 0)
		canvas.create_rounded_box(
							348.0, # type: ignore
							43.0, # type: ignore
							1182.0, # type: ignore
							636.0, # type: ignore
							20, # type: ignore
							"white")

		canvas.create_rounded_box(
			23.0, # type: ignore
			43.0, # type: ignore
			318.0, # type: ignore
			418.0, # type: ignore
			20, # type: ignore
			"white")

		canvas.create_text(
			510.0,
			7.0,
			anchor="nw",
			text="Wind turbines management interface",
			fill="#000000",
			font=myfont24
		)

		canvas.create_text(
			32.0,
			73.0,
			anchor="nw",
			text="Administration Zone",
			fill="#000000",
			font=myfont24
		)

		canvas.create_text(
			94.0,
			150.0,
			anchor="nw",
			text="Electricity production",
			fill="#000000",
			font=myfont16
		)

		def enable_electricity_production():
			self.server.enable_electricity_production(0)
			maintenance_string.set("Maintenance mode : OFF")

		def disable_electricity_production():
			self.server.disable_electricity_production(0)

		button_image_1 = PhotoImage(
			file=relative_to_assets("button_1.png"))
		button_1 = Button(
			image=button_image_1,
			borderwidth=0,
			highlightthickness=0,
			command=enable_electricity_production,
			relief="flat"
		)
		button_1.place(
			x=29.0,
			y=169.0,
			width=135.0,
			height=59.0
		)

		button_image_2 = PhotoImage(
			file=relative_to_assets("button_2.png"))
		button_2 = Button(
			image=button_image_2,
			borderwidth=0,
			highlightthickness=0,
			command=disable_electricity_production,
			relief="flat"
		)
		button_2.place(
			x=177.0,
			y=169.0,
			width=135.0,
			height=59.0
		)

		canvas.create_text(
			94.0,
			246.0,
			anchor="nw",
			text="Maintenance mode",
			fill="#000000",
			font=myfont16
		)

		maintenance_string = StringVar()
		maintenance_string.set("Maintenance mode : ON ⚠️")

		maintenance_label = Label(
			anchor="nw",
			text=maintenance_string.get(),
			font=myboldfont16,
			background="#FFFFFF",
			padx=20.0,
			pady=20.0
			)

		maintenance_label.place(x=25.0, y=340.0)

		def enable_maintenance_mode():
			self.server.enable_maintenance_mode(0)
			maintenance_string.set("Maintenance mode : ON ⚠️")

		def disable_maintenance_mode():
			self.server.disable_maintenance_mode(0)
			maintenance_string.set("Maintenance mode : OFF")

		button_image_3 = PhotoImage(
			file=relative_to_assets("button_3.png"))
		button_3 = Button(
			image=button_image_3,
			borderwidth=0,
			highlightthickness=0,
			command=enable_maintenance_mode,
			relief="flat"
		)
		button_3.place(
			x=29.0,
			y=265.0,
			width=135.0,
			height=59.0
		)

		button_image_4 = PhotoImage(
			file=relative_to_assets("button_4.png"))
		button_4 = Button(
			image=button_image_4,
			borderwidth=0,
			highlightthickness=0,
			command=disable_maintenance_mode,
			relief="flat"
		)
		button_4.place(
			x=178.0,
			y=265.0,
			width=135.0,
			height=59.0
		)

		image_image_1 = PhotoImage(
			file=relative_to_assets("image_1.png"))
		image_1 = canvas.create_image(
			163.0,
			519.0,
			image=image_image_1
		)

		canvas.create_text(
			680,
			60,
			anchor="nw",
			text="Wind turbine 1",
			fill="#000000",
			font=myboldfont16
		)

		canvas.create_text(
			420,
			400,
			anchor="nw",
			text="Electricity production",
			fill="#000000",
			font=myfont16
		)

		# Wind turbine 1 electricity production gauge
		wt1_gauge1 = Gauge(window, padding=1)
		wt1_gauge1.pack()
		wt1_gauge1.arcvariable.trace_add('write', lambda *args, g=wt1_gauge1: g.textvariable.set("ON" if g.arcvariable.get() == 360 else "OFF" if g.arcvariable.get() == 0 else f'{g.arcvariable.get()} OFF'))
		ttk.Scale(window, from_=0, to=360) # type: ignore
		wt1_gauge1.troughcolor = '#CF1B1B'
		wt1_gauge1.indicatorcolor = '#58BC2A'
		wt1_gauge1.place(x=400, y=115)

		canvas.create_text(
			690,
			400,
			anchor="nw",
			text="Rotation speed",
			fill="#000000",
			font=myfont16
		)

		# Wind turbine 1 rotation speed gauge
		wt1_gauge2 = Gauge(window, padding=1, background='#FFFFFF')
		wt1_gauge2.pack()
		wt1_gauge2.arcvariable.trace_add('write', lambda *args, g=wt1_gauge2: g.textvariable.set(f'{g.arcvariable.get()} tr/min'))
		ttk.Scale(window, from_=0, to=360) # type: ignore
		wt1_gauge2.place(x=650, y=115)

		canvas.create_text(
			950,
			400,
			anchor="nw",
			text="Wind speed",
			fill="#000000",
			font=myfont16
		)

		wt1_gauge3 = Gauge(window, padding=1, background='#FFFFFF')
		wt1_gauge3.pack()
		wt1_gauge3.arcvariable.trace_add('write', lambda *args, g=wt1_gauge3: g.textvariable.set(f'{g.arcvariable.get()} km/h'))
		ttk.Scale(window, from_=0, to=360) # type: ignore
		wt1_gauge3.place(x=900, y=115)

		canvas.create_text(
			420,
			90,
			anchor="nw",
			text="Electricity production",
			fill="#000000",
			font=myfont16
		)

		canvas.create_text(
			690,
			370,
			anchor="nw",
			text="Wind turbine 2",
			fill="#000000",
			font=myboldfont16
		)

		# Wind turbine 2 electricity production gauge
		wt2_gauge1 = Gauge(window, padding=1, background='#FFFFFF')
		wt2_gauge1.pack()
		wt2_gauge1.arcvariable.trace_add('write', lambda *args, g=wt2_gauge1: g.textvariable.set("ON" if g.arcvariable.get() == 360 else "OFF" if g.arcvariable.get() == 0 else f'{g.arcvariable.get()} OFF'))
		ttk.Scale(window, from_=0, to=360) # type: ignore
		wt2_gauge1.troughcolor = '#CF1B1B'
		wt2_gauge1.indicatorcolor = '#58BC2A'
		wt2_gauge1.place(x=400, y=425)

		canvas.create_text(
			680,
			90,
			anchor="nw",
			text="Rotation speed",
			fill="#000000",
			font=myfont16
		)

		# Wind turbine 2 rotation speed gauge
		wt2_gauge2 = Gauge(window, padding=1, background='#FFFFFF')
		wt2_gauge2.pack()
		wt2_gauge2.arcvariable.trace_add('write', lambda *args, g=wt2_gauge2: g.textvariable.set(f'{g.arcvariable.get()} tr/min'))
		ttk.Scale(window, from_=0, to=360) # type: ignore
		wt2_gauge2.place(x=650, y=425)

		canvas.create_text(
			950,
			90,
			anchor="nw",
			text="Wind speed",
			fill="#000000",
			font=myfont16
		)

		# Wind turbine 2 wind speed gauge
		wt2_gauge3 = Gauge(window, padding=1, background='#FFFFFF')
		wt2_gauge3.pack()
		wt2_gauge3.arcvariable.trace_add('write', lambda *args, g=wt2_gauge3: g.textvariable.set(f'{g.arcvariable.get()} km/h'))
		ttk.Scale(window, from_=0, to=360) # type: ignore

		wt2_gauge3.place(x=900, y=425)

		window.resizable(False, False)

		window.title("Wind turbines management interface")

		def update_gauge():
			# Get values for Wind_Turbine_1
			turbine1_electricity_production, turbine1_maintenance_mode, turbine1_wind_direction, turbine1_rotation_speed, turbine1_wind_speed = self.client.get_node_value(self.client.turbine1)
			wt1_gauge1.arcvariable.set(360 if turbine1_electricity_production else 0)
			wt1_gauge2.arcvariable.set(turbine1_rotation_speed)
			wt1_gauge3.arcvariable.set(turbine1_wind_speed)

			# Get values for Wind_Turbine_2
			turbine2_electricity_production, turbine2_maintenance_mode, turbine2_wind_direction, turbine2_rotation_speed, turbine2_wind_speed = self.client.get_node_value(self.client.turbine2)
			wt2_gauge1.arcvariable.set(360 if turbine2_electricity_production else 0)
			wt2_gauge2.arcvariable.set(turbine2_rotation_speed)
			wt2_gauge3.arcvariable.set(turbine2_wind_speed)
			maintenance_label.config(text=maintenance_string.get())
			window.after(200,update_gauge)

		window.after(10,update_gauge)
		window.mainloop()

	def run(self):
		if self.mode == "exploitation":
			# Start the server and client in separate threads
			server_thread = threading.Thread(target=self.run_exploitation_server)
			client_thread = threading.Thread(target=self.run_exploitation_client)

			server_thread.start()
			time.sleep(1)
			client_thread.start()
			time.sleep(1)

			# Once both server and client threads finish, start the GUI
			self.run_gui()
		else:
			# Start the server and client in separate threads
			server_thread = threading.Thread(target=self.run_mitigation_server)
			client_thread = threading.Thread(target=self.run_mitigation_client)

			server_thread.start()
			time.sleep(1)
			client_thread.start()
			time.sleep(1)

			# Once both server and client threads finish, start the GUI
			self.run_gui()
