import serial
import time
cmdHdr=[]
cmdLenSet=0
cmdLenGet=0
dataBufSet=""
dataBufGet=""
statusWordSet=""
statusWordGet=""
##########################################Initialize Serial Port#############################################
def initPort(portNum,baud):
    global ser
    ser=serial.Serial(port=portNum,baudrate=baud,timeout=1)
    return ser

ser=initPort('COM5',57600)
##########################################Read Byte From File###################################################
def readByteFromFile(filename,lineno,offset):
    if offset==0:
        with open(filename,'r') as f:
            lines=f.readlines()
        return (lines[lineno][offset],lines[lineno][offset+1])

    else:
        with open(filename,'r') as f:
            offset=offset*3                                           ##if there is no spacing in command then use offset=offset*2
            lines=f.readlines()
        return (lines[lineno][offset],lines[lineno][offset+1])



#print("".join(readByteFromFile('data.txt',0,1)))

#########################################Read Line From File####################################################
def readLineFromFile(filename,lineno):
    with open(filename,'r') as f:
        lines=f.readlines()
    return lines[lineno]

#print(readLineFromFile('data.txt',1))

#readFileLine=readLineFromFile('data.txt',1)
#print(readFileLine)
#print(type(readFileLine))

# a=readFileLine.split(" ")
# print(a)
# cmd=[]
# for i in range(len(a)):
#     cmd.append(int(a[i],16))
# print(cmd)

####################################Conversion of string received from file to int#################################
def cmdToInt(cmd):
    a=cmd.split(" ")
    cmd_int=[]
    for i in range(len(a)):
        cmd_int.append(int(a[i],16))
    return cmd_int

#print(cmdToInt(readFileLine))
#intCmd=cmdToInt(readFileLine)

######################################Conversion of int cmd to hex form#############################################
def intToHex(cmd):
    cmd_hex=[]
    for i in range(len(cmd)):
        cmd_hex.append(hex(cmd[i]))
    return cmd_hex

#print(intToHex(intCmd))

#############################################Check type of Command##################################################
def checkCmd(cmd):
    if cmd[4] == "0x0" and cmd[5] == "0x10" and cmd[1] == "0x2d":  # Read Sign Data
        return 1                                              #1-> out 0->IN
    elif cmd[4] == "0x2" and cmd[5] == "0x0" and cmd[1] == "0xa2":  # get Current page info
        return 1
    elif cmd[4] == "0x1" and cmd[5] == "0x0" and cmd[1] == "0x2b":  # calculate CRC
        return 1
    elif cmd[4] == "0x0" and cmd[5] == "0x10" and cmd[1] == "0xd2":  # Read Serial Number
        return 1
    elif cmd[4] == "0xe" and cmd[5] == "0x0" and cmd[1] == "0xe0":  # Create Block
        return 0
    elif cmd[4] == "0xc" and cmd[5] == "0x0" and cmd[1] == "0x3d":  # Update block page
        return 0
    elif cmd[4] == "0x0" and cmd[5] == "0x2" and cmd[1] == "0xa4":  # Select block
        return 0
    elif cmd[4] == "0x0" and cmd[5] == "0x2" and cmd[1] == "0xa6":  # Display Sign Info
        return 0
    elif cmd[4] == "0x0" and cmd[5] == "0x2" and cmd[1] == "0xe4":  # Signboard Erase
        return 0
    elif cmd[4] == "0x0" and cmd[5] == "0x2" and cmd[1] == "0xa8":  # Flipblock
        return 0
    else:
        pass


###################################################Set and Get Command Header#####################################################
def setCmdHdr(cmd):
    global cmdHdr
    for i in range(len(cmd)):
        cmdHdr=cmd
    return cmdHdr

def getCmdHdr():
    global cmdHdr
    global getCmdBuff
    for i in range(len(cmdHdr)):
        getCmdBuff=cmdHdr
    return getCmdBuff

#################################################Set and Get Command Length#######################################################
def setCmdLength(cmd):
    global cmdLenSet
    cmdLenSet=cmd[4:6]
    return cmdLenSet

def getCmdLength():
    global cmdLenSet
    global cmdLenGet
    cmdLenGet=cmdLenSet
    return cmdLenGet

#################################################Set and Get Data Bufer############################################################
def setDataBuff(cmd):
    global dataBufSet
    dataBufSet=cmd[6:]
    return dataBufSet

def getDataBuff():
    global dataBufSet
    global dataBufGet
    dataBufGet=dataBufSet
    return dataBufGet

###############################################Status Word Buffer#################################################################
def setSw1Sw2(cmd):
    pass

def getSw1Sw1():
    pass

##############################################Send Command#########################################################################
def sendCmd(mode):
    ser.write(serial.to_bytes(intCmd[0:6]))
    time.sleep(0.5)

    if mode==0:
        global ack
        ack=ser.read(1)
        data=getDataBuff()
        ser.write(serial.to_bytes(data))
    return ack

###############################################Receive Command######################################################################
def recvCmd(mode):
    ser.write(serial.to_bytes(intCmd))
    time.sleep(0.5)
    if mode==None:
        data_recv=ser.read(2)
        return data_recv
    elif mode==1:
        ser.write(serial.to_bytes(intCmd))
        time.sleep(1)
        data=b''
        timeout=time.time()+3.0
        while ser.inWaiting() or time.time()-timeout<0.0:
            if ser.inWaiting()>0:
                data+=ser.read(ser.inWaiting())
                timeout=time.time()+3.0
        return data
    elif mode==0:
        ser.write(serial.to_bytes(getDataBuff()))
        resp=ser.read(2)
        return resp
# readFileLine=readLineFromFile('data.txt',0)
# intCmd = cmdToInt(readFileLine)
# print(intToHex(intCmd))

readFileLine=readLineFromFile('data.txt',1)
intCmd = cmdToInt(readFileLine)
cmdHex=intToHex(intCmd)
print(intToHex(intCmd))
cmdCheck=checkCmd(cmdHex)
print("cmd type: ",cmdCheck)
# ser.write(serial.to_bytes(intCmd))
# time.sleep(1)
# data=b''
# timeout=time.time()+3.0
# while ser.inWaiting() or time.time()-timeout<0.0:
#     if ser.inWaiting()>0:
#         data+=ser.read(ser.inWaiting())
#         timeout=time.time()+3.0
# data_left=ser.inWaiting()
# data+=ser.read(data_left)
ser.flushInput()
#print("Response: ",hex(int.from_bytes(data,byteorder='little')))
#print(setCmdHdr(intCmd))
print("Set Cmd Hdr: ",setCmdHdr(intCmd))
#setHdrcmd=setCmdHdr(intCmd)
print("Get Cmd Hdr: ",getCmdHdr())
#print("Get: ",getCmdHdr(setHdrcmd))
print("Set Cmd Len: ",setCmdLength(cmdHex))
print("Get Cmd Len: ",getCmdLength())
#a=setCmdLength(intCmd)
#print(getCmdLength(a))
print("Set Data Buff: ",setDataBuff(intCmd))
print("Get Data Buff: ",getDataBuff())
#ack=sendCmd(cmdCheck)
#print("Ack: ",hex(int.from_bytes(ack,byteorder='little')))
resp=recvCmd(cmdCheck)
print("Resp: ",hex(int.from_bytes(resp,byteorder='little')))



# readFileLine=readLineFromFile('data.txt',3)
# intCmd = cmdToInt(readFileLine)
# print(intToHex(intCmd))
#
# readFileLine=readLineFromFile('data.txt',4)
# intCmd = cmdToInt(readFileLine)
# print(intToHex(intCmd))



