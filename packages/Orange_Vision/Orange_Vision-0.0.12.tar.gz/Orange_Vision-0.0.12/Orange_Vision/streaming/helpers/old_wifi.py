import subprocess
import csv
import os
from wifi import Cell, Scheme

def search_wifi():
    wifi_list = {}
    cells = Cell.all('wlan0')
    for connection in cells:
        SSID = connection.ssid
        enc = connection.encrypted
        if SSID:
            wifi_list[SSID] = enc

    return wifi_list




def write_previous_connections(SSID):
    ssids = read_json('previous')
    if SSID not in ssids:

        ssids.append(SSID)
    
    write_json('previous', ssids)


def search_connected():
    process = subprocess.Popen(['nmcli', 'd'], stdout=subprocess.PIPE)
    #process = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)

    stdout, stderr = process.communicate()
    #print(stdout.decode('utf-8').splitlines())
    reader = csv.DictReader(stdout.decode('utf-8').splitlines(),
                            delimiter=' ', skipinitialspace=True,
                            fieldnames=['NAME', 'UUID',
                                        'TYPE', 'DEVICE',])

    wifi_list = {}
    connected = {'connection' : False}
    for row in reader:
        if row ['TYPE'] == 'wifi':
            uuid = row['UUID']
            name = row['NAME']
            wifi_list[name] = connection
    return connected, wifi_list


#  nmcli d up <name>
def disconnect(wifi_name):
    os.system(f'nmcli con down id {wifi_name}')

def request_password():
    # send a socket requesting a password
    return False

def connect_wifi(name, password=None):

    previous =  read_json('previous')
    print(previous, "previous")
   
    if name in previous:
         os.system(f'nmcli c up {name}')
    else:
        os.system(f'nmcli device wifi connect {name} password {password}')

    # if password == None:
    
    #     process = subprocess.Popen(['nmcli', 'c', 'up', name], stdout=subprocess.PIPE)
        
    #     stdout, stderr = process.communicate()
    #     read = stdout.decode('utf-8')
    #     print(read)
    #     if len(read) == 0:
    #         return request_password()
    #     return True
    # 



class Finder:
    def __init__(self, *args, **kwargs):
        self.server_name = kwargs['server_name']
        self.password = kwargs['password']
        self.interface_name = kwargs['interface']
        self.main_dict = {}

    def run(self):

        os.system(f'sudo rm -rf /etc/NetworkManager/system-connections/*{self.server_name}*')
        command = """sudo iwlist wlan0 scan | grep -ioE 'ssid:"(.*{}.*)'"""
        result = os.popen(command.format(self.server_name))
        result = list(result)
        if "Device or resource busy" in result:
                return None
        else:
            ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
            print("Successfully get ssids {}".format(str(ssid_list)))

        for name in ssid_list:
            try:
                result = self.connection(name)
            except Exception as exp:
                print("Couldn't connect to name : {}. {}".format(name, exp))
            else:
                if result:
                    print("Successfully connected to {}".format(name))

    def connection(self, name):
        try:
            os.system("nmcli d wifi connect {} password {} iface {}".format(name,
       self.password,
       self.interface_name))
        except:
            raise
        else:
            return True

if __name__ == "__main__":
    # Server_name is a case insensitive string, and/or regex pattern which demonstrates
    # the name of targeted WIFI device or a unique part of it.
    server_name = "Tech-Garage6-5G"
    password = "techgrocks"
    interface_name = "wlan0" # i. e wlp2s0  
    F = Finder(server_name=server_name,
               password=password,
               interface=interface_name)
    F.run()