import serial
import time
#ser=serial.Serial(port='COM5',baudrate=57600)
cmd_hdr=[]
#test1=[0xA1,0xD0,0x00,0x00,0x00,0x00]
#test1=[0xA1,0xE0,0x00,0x00,0x0E,0x00,0x80,0x02,0x01,0x00,0x81,0x04,0x52,0x00,0x00,0x00,0x82,0x02,0x01,0x00]
#test1=[0xA1,0x2D,0x00,0x00,0x00,0x10]
test1=[0xA1,0x3D,0x00,0x01,0x0C,0x00,0x01,0x10,0x60,0x0A,0x00,0x01,0x01,0x00,0x00,0x46,0x00,0x01]
#test1=[0xA1,0x2D,0x00,0x00,0x00,0x00]
#test1=[0xA1,0xA8,0x00,0x00,0x00,0x00]

print("cmd: ",test1)
test2=[]
cmd_length_get=0
cmd_length_set=0
data_buff_get=""
data_buff_set=""
test_buf_data="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
test_status_word="E0"
status_word_get=""
status_word_set=""
#############################Initialize Serial Port#######################################
def initPort(portNum,baud):
    global ser
    ser=serial.Serial(port=portNum,baudrate=baud,timeout=1.0)
    return ser

ser=initPort('COM5',57600)

##########################Check type of command###########################################
def checkCmd(cmd):
    if cmd[4] == 0x00 and cmd[5] == 0x10 and cmd[1] == 0x2D:  # Read Sign Data
        return 1                                              #1-> out 0->IN
    elif cmd[4] == 0x02 and cmd[5] == 0x00 and cmd[1] == 0xA2:  # get Current page info
        return 1
    elif cmd[4] == 0x01 and cmd[5] == 0x00 and cmd[1] == 0x2B:  # calculate CRC
        return 1
    elif cmd[4] == 0x00 and cmd[5] == 0x10 and cmd[1] == 0xD2:  # Read Serial Number
        return 1
    elif cmd[4] == 0x0E and cmd[5] == 0x00 and cmd[1] == 0xE0:  # Create Block
        return 0
    elif cmd[4] == 0x0C and cmd[5] == 0x00 and cmd[1] == 0x3D:  # Update block page
        return 0
    elif cmd[4] == 0x00 and cmd[5] == 0x02 and cmd[1] == 0xA4:  # Select block
        return 0
    elif cmd[4] == 0x00 and cmd[5] == 0x02 and cmd[1] == 0xA6:  # Display Sign Info
        return 0
    elif cmd[4] == 0x00 and cmd[5] == 0x02 and cmd[1] == 0xE4:  # Signboard Erase
        return 0
    elif cmd[4] == 0x00 and cmd[5] == 0x02 and cmd[1] == 0xA8:  # Flipblock
        return 0
    else:
        pass

cmdchk=checkCmd(test1)
print("command type: ",cmdchk)

############################# Get and Set Command Header##################################
def setCmdHeader(t1):
    global cmd_hdr
    for i in range(len(t1)):
        cmd_hdr=t1
    return cmd_hdr


def getCmdHeader(t2):
    global test2
    for i in range(len(t2)):
        test2=cmd_hdr
    return test2



setHdrCmd=setCmdHeader(test1)

#print(setHdrCmd)

getHdrCmd=getCmdHeader(setHdrCmd)
#print(getHdrCmd)
#print(getCmdHeader(setHdrCmd))

########################### Get and Set command Length#####################################
def setCmdLength(cmd):
    global cmd_length_set
    cmd_length_set=cmd[4:6]
    return cmd_length_set

def getCmdLength(cmd):
    global cmd_length_get
    cmd_length_get=cmd_length_set
    return cmd_length_get

#print(setCmdLength(test1))
setcmdlen=setCmdLength(test1)
getcmdlen=getCmdLength(setcmdlen)
#print(getcmdlen)

########################## Get and Set Data Buffer#########################################

def setDataBuff(data):
    #global test_buf_data
    global data_buff_set
    #data_buff_set=data
    data_buff_set=data[6:]
    return data_buff_set

def getDataBuff():
    global data_buff_get
    data_buff_get=data_buff_set
    return data_buff_get

#setdatabuffer=setDataBuff(getcmdlen)
#print(setdatabuffer)
setdatabuffer=setDataBuff(getHdrCmd)
#print(getDataBuff())
#############################Status Word Buffer###################################

def setSw1Sw2(status):
    global test_status_word
    global status_word_set
    status_word_set=test_status_word
    return status_word_set

def getSw1Sw2():
    global status_word_get
    status_word_get=status_word_set
    return status_word_get

# print(setSw1Sw2(test_status_word))
# print(getSw1Sw2())


#################################Send command########################################
def sendCmd(mode):
    ser.write(serial.to_bytes(getHdrCmd[0:6]))
    time.sleep(0.5)

    if mode==0:                                                                         #acknowledgement will only comes from input command
        ack=ser.read(1)
        print("Ack: ", hex(int.from_bytes(ack,byteorder='little')))
        data=getDataBuff()
        ser.write(serial.to_bytes(data))
    return ''
print(sendCmd(cmdchk))

###############################Receive Data###########################################
def recvCmd(mode):
    global data,data_left,data_recv
    ser.write(serial.to_bytes(getHdrCmd))
    time.sleep(0.5)
    #data_recv=ser.read(2)
    if mode==None:
        data_recv=ser.read(2)
        print("Response: ",hex(int.from_bytes(data_recv,byteorder='little')))
    elif mode==1:
        ser.write(serial.to_bytes(getHdrCmd))
        time.sleep(1)
        data=b""
        timeout = time.time() + 3.0
        while ser.inWaiting() or time.time()-timeout<0.0:
            if ser.inWaiting()>0:
                data+=ser.read()
                timeout=time.time()+3.0
            else:
                print("waiting!!")
        # ser.flushInput()
        # data=ser.read()
        # data_left=ser.inWaiting()
        # data+=ser.read(data_left)
        ser.flushInput()
        print("Response: ",hex(int.from_bytes(data,byteorder='little'))[0:6])
        print("Data: ",hex(int.from_bytes(data,byteorder='big')))
    elif mode==0:
        ser.write(serial.to_bytes(getDataBuff()))
        resp=ser.read(2)
        ser.timeout=1
        print("Response: ",hex(int.from_bytes(resp,byteorder='little')))
    return exit(0)


    #return ''

print(recvCmd(cmdchk))
# def recvCmd(mode):
#     sendCmd(mode)
