
import time
import sched
import subprocess
atStation = '192.168.100.75'
ifconfigCommand = "ifconfig en13 | grep 'inet ' | awk '{print $2}'"
edifierStatusCommand = "blueutil --is-connected '04-fe-a1-a2-fe-f8'"
edifierConnectCommand = "blueutil --connect '04-fe-a1-a2-fe-f8'"
edifierDisconnectCommand = "blueutil --disconnect '04-fe-a1-a2-fe-f8'"

s = sched.scheduler(time.time, time.sleep)


def timerInterval(sc):

    getCurrentIP = subprocess.run(
        [ifconfigCommand], shell=True, text=True, capture_output=True)
    currentIP = getCurrentIP.stdout.strip()

    checkConnectedBT = subprocess.run(
        [edifierStatusCommand], shell=True, text=True, capture_output=True)
    edifierStatus = checkConnectedBT.stdout.strip()

    if currentIP == atStation and edifierStatus == '0':
        print("At station, Connecting")
        print("Current IP is: ", currentIP)
        subprocess.run(
            [edifierConnectCommand], shell=True)

    if currentIP != atStation and edifierStatus == '1':
        print("left station, Disconecting")
        print("Current IP is: ", currentIP)
        subprocess.run(
            [edifierDisconnectCommand], shell=True)

    s.enter(20, 1, timerInterval, (sc,))


s.enter(20, 1, timerInterval, (s,))
s.run()
