from threading import Timer
from subprocess import run

# To Find out the Devices ID run: blueutil --connected
BT_device_ID = "'04-fe-a1-a2-fe-f8'"
# Must be static IP
station_IP = ["192.168.100.50", "192.168.150.50"]
# uses ifconfig to print all the IPV4 Addresses from all the interfaces
get_IPv4_address = "ifconfig | grep 'inet ' | awk '{print $2}'"
# blueutil commands
blueutil = "/opt/homebrew/bin/blueutil"
blueutil_is_connected = f"{blueutil} --is-connected {BT_device_ID}"
blueutil_connect = f"{blueutil} --connect {BT_device_ID}"
blueutil_disconnect = f"{blueutil} --disconnect {BT_device_ID} --wait-disconnect {BT_device_ID}"

print("Started BT-Connect")


def at_station():
    IPList = run([get_IPv4_address], shell=True, text=True, capture_output=True).stdout.strip().split("\n")
    ## Debug - prints the list of the IPs from ifconfig command
    # print(IPList)
    for ip in station_IP:
        if ip in IPList:
            return True
    return False


# Thread loop to run every defined time in seconds
def runEvery():
    Timer(20.0, runEvery).start()
    # Class That returns True of the Ip Maching from Interfaces

    # Returns 1 if BT Device connected 0 if disconnected
    BT_Connection = run([blueutil_is_connected], shell=True, text=True, capture_output=True).stdout.strip()
    # Sets true/false to "at_stationStatus" every run
    at_stationStatus = at_station()

    if at_stationStatus and BT_Connection == "0":
        print("At station, connecting.")
        run([blueutil_connect], shell=True)

    elif not at_stationStatus and BT_Connection == "1":
        print("left station - disconnecting.")
        run([blueutil_disconnect], shell=True)


runEvery()
