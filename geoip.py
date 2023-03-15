import ipaddress
import json
import time


class GeolocationDB:
    def __init__(self):
        with open("ips/ip_dct.json", "r") as f:
            self.ip_dct = json.loads(f.read())
            
    def IPToGeolocation(self, address):
        try:
            address = int(ipaddress.IPv4Address('{}'.format(address)))
            subnets = self.ip_dct[str(address)[:4]]
            subnets2 = subnets[str(address).split(str(address)[:4])[1][:2]]
            for subnet in subnets2:
                data = subnet.split(",")
                lower_address, upper_address = int(data[0]), int(data[1])
                if lower_address < address:
                    if upper_address > address:
                        data = subnets2[subnet].split(",")
                        print(data)
                        return {"country":data[2], "region":data[3], "city":data[5], "lat":data[7], "lon":data[8]}
            raise Exception
        except Exception as e:
            return {"country":"?", "region":"?", "city":"?", "lat":"?", "lon":"?"}






