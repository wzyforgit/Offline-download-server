import urllib.request
import multiprocessing
import json
import os

def check(userName,fileName):
    if not os.path.exists(userName):
        return 1
    os.chdir(userName)

    try:
        with open(fileName+'.json','r') as f:
            obj = json.load(f)
            return obj['status']
    except:
        return 2
    finally:
        os.chdir('..')

def downloadFun(userName,url,fileName):
    if not os.path.exists(userName):
        os.makedirs(userName)
    os.chdir(userName)
    logfile=fileName+'.json'
    with open(logfile,'w') as f:
        json.dump({'status' : 'False'},f)

    try:
        urllib.request.urlretrieve(url,fileName)
    except:
        with open(logfile,'w') as f:
            json.dump({'status' : 'Fail'},f)
            os.chdir('..')
            return

    with open(logfile,'w') as f:
        json.dump({'status' : 'True'},f)

    os.chdir('..')

def startDownload(userName,url,fileName):
    p = multiprocessing.Process(target=downloadFun,args=(userName,url,fileName))
    p.start()
    if __name__ == '__main__':
        p.join()

if __name__ == '__main__':
    #startDownload('fuko','https://www.python.org/ftp/python/3.6.2/python-3.6.2-amd64.exe','196.exe')
    startDownload('fuko','https://www.bilibili.com','196.html')