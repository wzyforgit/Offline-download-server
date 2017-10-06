import UserManager
import server
import httpserver

import os
import sys
import socket
import signal

def startExitSignalWatcher(httpServerPid):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(('127.0.0.1',6000))
        s.listen(1)
    except:
        print('Fail to start ExitSignalWatcher')
        os.system('kill %d' % httpServerPid)
        os._exit(0)
    exitCode = b'abort'
    while(True):
        sock,addr = s.accept()
        data = sock.recv(1024)
        sock.close()
        if (not data) or data != exitCode:
            continue
        else:
            os.system('kill %d' % httpServerPid)
            os._exit(0)

def createGuard():
    pid = os.fork()
    if pid > 0:
        os._exit(0)
    else:
        os.chdir('.')
        os.setsid()
        os.umask(0)
        pid = os.fork()
        if pid > 0:
            os._exit(0)
        else:
            signal.signal(signal.SIGCHLD,signal.SIG_IGN)
            server.startServer()
            httpServerPid = httpserver.startDownloadServer()
            startExitSignalWatcher(httpServerPid)

def closeGuard():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('127.0.0.1',6000))
        s.send(b'abort')
        s.close()
    except:
        print('close server fail')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'start':
            createGuard()
        elif sys.argv[1] == 'abort':
            closeGuard()
        elif sys.argv[1] == 'addUser':
            if len(sys.argv) >= 4:
                userName = sys.argv[2]
                userPsw = sys.argv[3]
                UserManager.createNewUser(userName,userPsw)
        else:
            print('Unknown order,please retry')
    else:
        print('No order')