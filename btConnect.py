
import time
import sched
import subprocess
atStation = '192.168.100.75'
en5Command = "ifconfig en5 | grep 'inet ' | awk '{print $2}'"
edifierStatusCommand = "blueutil --is-connected '04-fe-a1-a2-fe-f8'"
edifierConnectCommand = "blueutil --connect '04-fe-a1-a2-fe-f8'"
edifierDisconnectCommand = "blueutil --disconnect '04-fe-a1-a2-fe-f8'"
lastIP = ''

s = sched.scheduler(time.time, time.sleep)


def timerInterval(sc):
    global lastIP

    getCurrentIP = subprocess.run(
        [en5Command], shell=True, text=True, capture_output=True)
    currentIP = getCurrentIP.stdout.strip()

    checkConnectedBT = subprocess.run(
        [edifierStatusCommand], shell=True, text=True, capture_output=True)
    edifierStatus = checkConnectedBT.stdout.strip()

    if currentIP != lastIP and currentIP == atStation:
        print("At Station - Connect")
        print("lastIP is: ", lastIP)
        print("currentIP is: ", currentIP)
        subprocess.run(
            [edifierConnectCommand], shell=True)

    if currentIP == atStation and currentIP == lastIP and edifierStatus == '0':
        print("Same IP Not Connected")
        print("lastIP is: ", lastIP)
        print("currentIP is: ", currentIP)
        subprocess.run(
            [edifierConnectCommand], shell=True)

    if currentIP != lastIP and currentIP != atStation:
        print("left Station - Dissconed")
        print("lastIP is: ", lastIP)
        print("currentIP is: ", currentIP)
        subprocess.run(
            [edifierDisconnectCommand], shell=True)

    lastIP = currentIP

    s.enter(20, 1, timerInterval, (sc,))


s.enter(20, 1, timerInterval, (s,))
s.run()
