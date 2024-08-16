from tkinter import *
from tkinter import ttk
from r2300_functions import *
from PIL import Image, ImageTk

network = read_ip()

# create GUI root
root = Tk()
root.title ("R2300")
root.geometry ("500x500")
icon = PhotoImage(file="paf.png")
sensor_image = ImageTk.PhotoImage(file="r2300.png")
root.iconphoto(True,icon)

# create Network Setup Frame
network = ttk.Frame(root, padding=10, width=200, height=200, borderwidth=1)
network.grid()

sensor_image_label = ttk.Label(root, padding = 100, image=sensor_image)
sensor_image_label.image = sensor_image
sensor_image_label.grid(column=2, row=0)

network_setup_label = ttk.Label(network, text="Network Setup: ", padding=5, font=("Arial", 9, "bold")).grid(column=0, row=0)

sensor_ip_address_label = ttk.Label(network, text="sensor_ip_address:", padding=5).grid(column=0,row=1)
sensor_ip_address_entry = ttk.Entry(network)
sensor_ip_address_entry.grid(column=0,row=2)

pc_ip_address_label = ttk.Label(network, text="pc_ip_address:", padding=5).grid(column=0,row=3)
pc_ip_address_entry = ttk.Entry(network)
pc_ip_address_entry.grid(column=0,row=4)

save_label = ttk.Button(network, text="SAVE", padding=5, width=5, command=lambda: save_ip(sensor_ip_address_entry.get(), pc_ip_address_entry.get())).grid(column=0,row=5)

read_label = ttk.Button(network, text="READ", padding=5, width=5, command=lambda: check_ip()).grid(column=0,row=6)

get_protocol_info_bt = ttk.Button(network, text="get_protocol_info",width=20, padding=5, command=lambda: send_request(http_commands('get_protocol_info'))).grid(column=0,row=7)

get_parameter_bt = ttk.Button(network, text="get_parameter",width=20, padding=5, command=lambda: send_request(http_commands('get_parameter?'))).grid(column=0,row=8)

request_handle_bt = ttk.Button(network, text="request_handle",width=20, padding=5, command=lambda: request_handle(http_commands('request_handle_udp?address='+ read_ip()[1] + '&port=6464&packet_type=C1'))).grid(column=0,row=9)

start_scanoutput_bt = ttk.Button(network, text="start_scanoutput",width=20, padding=5, command=lambda: send_request(http_commands('start_scanoutput?handle='+ read_handle()))).grid(column=0,row=10)

stop_scanoutput_bt = ttk.Button(network, text="stop_scanoutput",width=20, padding=5, command=lambda: send_request(http_commands('stop_scanoutput?handle='+ read_handle()))).grid(column=0,row=11)

release_handle_bt = ttk.Button(network, text="release_handle",width=20, padding=5, command=lambda: send_request(http_commands('release_handle?handle='+ read_handle()))).grid(column=0,row=12)

rawdata_bt = ttk.Button(network, text="view_raw_data",width=20, padding=5, command=lambda: socket_connect(read_ip()[1], 'connect' )).grid(column=0,row=13)


root.mainloop()


