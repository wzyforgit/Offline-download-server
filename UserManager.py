import json
import threading

import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

serverFile = 'ServerData.json'
userFile   = 'UserData.json'
locker = threading.Lock()

def lock(fun):
    def __lock(*args, **kwargs):
        locker.acquire()
        pr = fun(*args, **kwargs)
        locker.release()
        return pr
    return __lock

@lock
def readServerSetting():
    try:
        with open(serverFile,'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        return False

@lock
def initDb():
    with open(userFile,'w') as f:
        obj = {'fuko' : '123456'}
        json.dump(obj, f)

@lock
def createNewUser(userName,password):
    data = {}
    try:
        with open(userFile,'r') as f:
            data = json.load(f)
    except:
        initDb()
        createNewUser(userName,password)
        return
    data[userName] = password
    with open(userFile,'w') as f:
        json.dump(data,f)

@lock
def deleteUser(userName):
    data = {}
    try:
        with open(userFile,'r') as f:
            data = json.load(f)
    except:
        return False
    try:
        del data[userName]
    except:
        return False
    with open(userFile,'w') as f:
        json.dump(data,f)
    return True

@lock
def readUserData(userName):
    obj = {}
    try:
        with open(userFile,'r') as f:
            obj = json.load(f)
        psw = obj[userName]
    except:
        return None
    return psw

if __name__ == '__main__':
    initDb()
    createNewUser('nagisa','12345')
    print(readUserData('nagisa'))
    deleteUser('nagisa')
    print(readUserData('nagisa'))