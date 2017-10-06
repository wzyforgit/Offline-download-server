import http.server
import socketserver
import json
import multiprocessing

def runDownloadServer():
    downloadPort = 0
    address = ''
    with open('ServerData.json') as f:
        obj = json.load(f)
        downloadPort = obj['downloadPort']
        address = obj['IP']
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((address, downloadPort), handler) as httpd:
        httpd.serve_forever()

def startDownloadServer():
    p = multiprocessing.Process(target=runDownloadServer)
    p.start()
    return p.pid

if __name__ == '__main__':
    import time
    import os
    pid = startDownloadServer()
    print('running')
    time.sleep(10)
    print('sleep')
    os.system('kill %d' % pid)
    print('done')