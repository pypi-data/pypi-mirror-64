##Avaiables eviroment
commands = {
        1 : 'ping www.google.com', #Check connected networks
        2 : 'netsh wlan add profile filename = "{path}"', #Add profile of networks
        3 : 'netsh wlan delete profile name = "{ssid}"', #Delete profile of any networks
        4 : 'netsh wlan connect name = "{ssid}"', #Connect to network have name is "{ssid}"
        5 : 'netsh wlan disconnect', #Disconnect internet
        6 : 'netsh wlan show profile', #Show all profile of network saved in PC
        }
resultFail = {
        1 : 'Ping request could not find host www.google.com. Please check the name and try again.',
        2 : 'Error',
        3 : 'Error',
        4 : 'Error',
        5 : 'Error',
        6 : 'Error',
        }
##Lib
import XMLWirelessWindows as Wireless
import CommandWinPy as cmd
import time


##Programer
class WIFI(object):
    def __init__(self):
        self.path = ""
        pass

    def run(self, ssid, passwd, authen = 'WAP2SPK', encryp = 'AES'):
        XML = Wireless.XML(ssid, passwd, authen, encryp)
        XML.initFile()
        cmd.commands(commands[2].replace("{path}", XML._path))
        cmd.commands(commands[4].replace("{ssid}", ssid))
        time.sleep(1.895)
        shell = cmd.commands(commands[1])
        if resultFail[1] in shell:
            print("[-] password is {} not corrent".format(passwd))
            cmd.commands(commands[5])
            XML.delFile()
        else:
            print("[+] password is {} corrent".format(passwd))
            print("Successfull :))")
