from tgn_hue_lib import HueApi
import time

hue_bridge_ip = "192.168.0.34"
hue_bridge_user_id = "Hue Bridge User"

#ini api
hue = HueApi(ip=hue_bridge_ip,user=hue_bridge_user_id)

#list all Lights
print(*hue.get_light_list(), sep = "\n")

#Info of a specific lamp
print(hue.get_light("Hue Play left"))

#Set of a specific lamp (Light Name or ID or Number, Command, data)
hue.set_light("Hue Play left","enable","0")
hue.set_light("Hue Play left","brightness","254")
hue.set_light("Hue Play left","color",[0,255,0])
time.sleep(5)
hue.set_light("Hue Play left","color",[255,0,0])
time.sleep(5)
hue.set_light("Hue Play left","brightness","40")
time.sleep(5)
hue.set_light("Hue Play left","disable","0")
