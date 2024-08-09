import time
# import sys
# import signal

from pymata4 import pymata4
from time import sleep

count=0
trigpin=11
ecopin=12
ir1pin = 4
ir2pin = 5

servopin = 10  # servo attached to this pin
ledpin = 9

distance = 0
fanangle = 90

rotr = False
rotl = False

sonardetectcount = 0

board=pymata4.Pymata4()


# def signal_handler(sig, frame):
#     print('You pressed Ctrl+C!!!!')
#     if board is not None:
#         board.reset()
#     sys.exit(0)


# signal.signal(signal.SIGINT, signal_handler)

def sonar_callback(data):
    global distance
    distance = data[2]
    print("distance: ",distance)
    if distance<100:
        board.digital_write(ledpin, 1)
    # else:
    #     board.digital_write(ledpin, 2)        

def rotateservo(angle):
    board.servo_write(servopin, angle)
    sleep(0.015)


def ir1_callback(data):
    global rotr
    print("ir1: ",data)
    if data[2] == 0 and rotr == False:
        rotr = True
        for i in range(90,180):
            rotateservo(i)

def ir2_callback(data):
    global rotl
    print("ir1: ",data)
    if data[2] == 0 and rotl == False:
        rotl = True
        for i in range(180)[:90:-1]:
            rotateservo(i)            

board.set_pin_mode_servo(servopin)
# board.servo_write(SERVO_MOTOR, 0)
# sleep(0.015)

board.set_pin_mode_digital_output(ledpin)

# board.set_pin_mode_digital_input_pullup(ir1pin, ir1_callback)
# board.set_pin_mode_digital_input_pullup(ir2pin, ir2_callback)

board.set_pin_mode_digital_input(ir1pin)
board.set_pin_mode_digital_input(ir2pin)

# ขวาง=0
# ไม่ขวาง=1

# board.set_pin_mode_sonar(trigpin,ecopin,sonar_callback)
board.set_pin_mode_sonar(trigpin,ecopin)
while True:
    try:
        time.sleep(0.1)
        ir1 = board.digital_read(ir1pin)
        ir2 = board.digital_read(ir2pin)

        sonar = board.sonar_read(trigpin)
        distance = sonar[0]

        if ir1[0] == 0 and rotr == False:
            board.digital_write(ledpin, 1)
            rotr = True
            if fanangle != 179:
                if fanangle == 90:
                    for i in range(90,180):
                        fanangle = i
                        rotateservo(i)
                if fanangle == 1:
                    for i in range(0,180):
                        fanangle = i
                        rotateservo(i)

        if ir2[0] == 0 and rotl == False:
            board.digital_write(ledpin, 1)
            rotl = True
            if fanangle != 1:
                if fanangle == 90:
                    for i in range(90)[:0:-1]:
                        fanangle = i
                        rotateservo(i)            
                if fanangle == 179:
                    for i in range(180)[:0:-1]:
                        fanangle = i
                        rotateservo(i)             

        # print("ir1", ir1[0], "ir2", ir2[0])
        if ir1[0] == 1 and rotr == True:
            rotr = False
        if ir2[0] == 1 and rotl == True:
            rotl = False
        
        if distance >= 100 and rotr == False and rotl == False:
            sonardetectcount = 0
            board.digital_write(ledpin, 2)

        if distance < 100 and rotr == False and rotl == False:
            sonardetectcount += 1
            if sonardetectcount == 3:
                board.digital_write(ledpin, 1)
                if fanangle == 1:
                    for i in range(0,91):
                        fanangle = i
                        rotateservo(i)                
                if fanangle == 179:
                    for i in range(180)[:89:-1]:
                        fanangle = i
                        rotateservo(i)                
                sonardetectcount = 0
        # board.sonar_read(trigpin)

        # x=input("input : ")
        # if x=="1":
        #     for i in range(90,180):
        #         rotateservo(i)
        # elif x=="2":
        #     for i in range(180)[:90:-1]:
        #         rotateservo(i)
        # elif x=="3":
        #     for i in range(90)[:0:-1]:
        #         rotateservo(i)        
        # elif x=="4":
        #     for i in range(0, 90):
        #         rotateservo(i)                        
    except Exception:
        board.shutdown()