import UserManager
import json

import os
import sys
import socket
import threading
import sys
import download

import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

# first pack:
# 0:name len 
# 1:name
# 2:psw len
# 3:psw
# 4fuko6123456
def dealFirstPack(data):
    try:
        nameLen = data[0]
        name = data[1:nameLen+1].decode('utf-8')
        pswLen = data[nameLen+1]
        psw = data[nameLen+2:].decode('utf-8')
    except Exception as e:
        return 3

    realPsw = UserManager.readUserData(name)
    if realPsw == None:
        return 1
    elif realPsw != psw:
        return 2
    else:
        return name

#dealClient will close sock,this function just break and return
def dealAfterPack(sock,name):
    while True:
        src = sock.recv(1024)
        if not src:
            break
        dst = src.decode('utf-8')
        if dst.startswith('ls'):
            os.chdir(name)
            for eachFile in os.listdir():
                sock.send((eachFile+'\r\n').encode('utf-8'))
            os.chdir('..')
        elif dst.startswith('download'):
            preList = dst.split(' ')
            download.startDownload(name,preList[1],preList[2])
            sock.send(b'download start')
        elif dst.startswith('check'):
            preList = dst.split(' ')
            result = download.check(name,preList[1])
            if result == 1:
                sock.send(b'no download dir')
            elif result == 2:
                sock.send(b'read fail')
            else:
                sock.send(result.encode('utf8'))
        elif dst.startswith('get'):
            preList = dst.split(' ')
            result = download.check(name,preList[1])
            if not result in [1,2]:
                obj = UserManager.readServerSetting()
                if obj != False:
                    ip = obj['IP']
                    port = obj['downloadPort']
                    sock.send(('http://'+ip+(':%d'%port)+'/'+name+'/'+preList[1]).encode('utf-8'))
                else:
                    sock.send(b'server data error')
            else:
                sock.send(b'connot download this file')
        elif dst.startswith('del'):
            try:
                preList = dst.split(' ')
                os.remove(name+'/'+preList[1])
                sock.send(b'remove success')
            except:
                sock.send(b'remove fail')
        elif dst == 'exit':
            sock.send(b'Bye~')
            break
        else:
            sock.send(b'Unknow order')

def dealClient(sock,addr):
    try:
        data = sock.recv(1024)
        if not data:
            sock.close()
        else:
            firstPackResult = dealFirstPack(data)
            if firstPackResult == 1:
                sock.send(b'Unknown user')
            elif firstPackResult == 2:
                sock.send(b'psw error')
            elif firstPackResult == 3:
                sock.send(b'data error')
            else:
                sock.send(b'login in success')
                dealAfterPack(sock,firstPackResult)
    except Exception as e:
        pass
    sock.close()

def mainServer():
    obj = UserManager.readServerSetting()
    if obj == False:
        return
    ip = obj['IP']
    port = obj['port']
    key = obj['key']

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen(5)
    while(True):
        sock,addr = s.accept()
        clientThread = threading.Thread(target = dealClient,args = (sock,addr))
        clientThread.start()

def startServer():
    mainThread = threading.Thread(target = mainServer)
    mainThread.start()
    if __name__ == '__main__':
        mainThread.join()#just for debug

if __name__ == '__main__':
    mainServer()