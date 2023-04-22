import urllib.request
import requests
import json
from requests import put

class HueApi:
    def __init__(self, ip, user):
        self.ip = ip
        self.user = user

    def convert_xy_rgb(self, x, y, bri=1):
        z = 1.0 - x - y
        Y = Y = bri / 255.0
        X = (Y / y) * x
        Z = (Y / y) * z
        r = X * 1.656492 - Y * 0.354851 - Z * 0.255038
        g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
        b = X * 0.051713 - Y * 0.121364 + Z * 1.011530
        r = (12.92 * r) if (r <= 0.0031308) else ((1.0 + 0.055)* pow(r, (1.0 / 2.4)) - 0.055)
        g = (12.92 * g) if (g <= 0.0031308) else ((1.0 + 0.055)* pow(g, (1.0 / 2.4)) - 0.055)
        b = (12.92 * b) if (b <= 0.0031308) else ((1.0 + 0.055)* pow(b, (1.0 / 2.4)) - 0.055)
        r = max(0, min(1, r))
        g = max(0, min(1, g))
        b = max(0, min(1, b))
        return str([int(r * 255), int(g * 255), int(b * 255)])
        

    def convert_rgb_xy(self, red, green, blue):
        rawRed = red / 255
        rawGreen = green / 255
        rawBlue = blue / 255
        gammaRed = pow((rawRed + 0.055) / (1.0 + 0.055),2.4) if (rawRed > 0.04045) else (rawRed / 12.92)
        gammaGreen = pow((rawGreen + 0.055) / (1.0 + 0.055),2.4) if (rawGreen > 0.04045) else (rawGreen / 12.92)
        gammaBlue = pow((rawBlue + 0.055) / (1.0 + 0.055),2.4) if (rawBlue > 0.04045) else (rawBlue / 12.92)
        X = gammaRed * 0.664511 + gammaGreen * 0.154324 + gammaBlue * 0.162028
        Y = gammaRed * 0.283881 + gammaGreen * 0.668433 + gammaBlue * 0.047685
        Z = gammaRed * 0.000088 + gammaGreen * 0.072310 + gammaBlue * 0.986039
        if X + Y + Z == 0:
            return [0, 0]
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
        return [x, y]

    def get_light_list(self):
        url = "http://"+self.ip+"/api/"+self.user+"/lights"
        get_url= urllib.request.urlopen(url)
        if(str(get_url.getcode()) == "200"):
            cach = requests.get(url).content
            #print(cach.decode("UTF8"))
            t_cach = json.loads(cach.decode("UTF8"))
            num = 1
            out = []
            while(True):
                try:
                    lamp_num = t_cach[str(num)]
                    type = t_cach[str(num)]['type']
                    name = t_cach[str(num)]['name']
                    id = t_cach[str(num)]['uniqueid']
                    state = str(t_cach[str(num)]['state']['on'])
                    bri = str(t_cach[str(num)]['state']['bri'])
                    color = str(t_cach[str(num)]['state']['xy']).split("[")[1].split("]")[0]
                    color_rgb =  self.convert_xy_rgb(float(color.split(", ")[0]), float(color.split(", ")[1]), int(bri))
                    ct = str(t_cach[str(num)]['state']['ct'])
                    cach_data = (str(num)+"|"+type+"|"+name+"|"+id+"|"+state+"|"+bri+"|"+color+"|"+color_rgb+"|"+ct)
                except:
                    break
                num += 1
                out.append(cach_data)
            return(out)
        else:
            return("Bridge Offline")
    
    def enable(self, num_lamp):
        put(f'http://{self.ip}/api/{self.user}/lights/{num_lamp}/state',
            json={'on': True})

    def disable(self, num_lamp):
        put(f'http://{self.ip}/api/{self.user}/lights/{num_lamp}/state',
            json={'on': False})

    def change_brightness(self, brightness, num_lamp):
        put(f'http://{self.ip}/api/{self.user}/lights/{num_lamp}/state',
            json={'bri': brightness})

    def change_color(self, red, green, blue, num_lamp):
        put(f'http://{self.ip}/api/{self.user}/lights/{num_lamp}/state',
            json={'xy': self.convert_rgb_xy(red, green, blue)})
        
    def get_light(self, search):
        list_data = self.get_light_list()
        num = len(list_data)
        x = 0
        for x in range(num):
            cach = list_data[x]
            try:
                test = int(search)
                if(search+"|Extended" in cach):
                    return(cach)
            except:
                if(search in cach):
                    return(cach)
            x += 1

    def set_light(self,search,command,data):
        lamp_num = self.get_light(search).split("|")[0]
        if(command == "enable"):
            self.enable(lamp_num)
        if(command == "disable"):
            self.disable(lamp_num)
        if(command == "brightness"):
            self.change_brightness(int(data), lamp_num)
        if(command == "color"):
            self.change_color(data[0], data[1], data[2], lamp_num)

