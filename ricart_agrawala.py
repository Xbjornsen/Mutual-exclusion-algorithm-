#!/usr/bin/env python
import sys
import time
import threading
import socket
import json
import os

REPLY = 0
REQUEST = 1
WANTED = 0
HELD = 1
RELEASED = 2
BUFSIZE = 1024

class Ricart_Agrawala(object):

    def __init__(self):
        self.localProcInfo = {
                'procState':        None,
                'procAddr':         None,
                'numNodes':         None,
                'procTimestamp':    None
                
        }
        self.remoteAddresses = {}
        self.defferedQueue = []
        self.replyQueue = []        

    def node_init(self, procAddr, numNodes, remoteAddr):
        self.localProcInfo['procState']         = RELEASED
        self.localProcInfo['procAddr']          = procAddr
        self.localProcInfo['numNodes']          = numNodes
        
        i = 0
        for x in remoteAddr:
            self.remoteAddresses[i] = x
            i += 1

        listenerThread = threading.Thread(target= self.messageListener)
        listenerThread.start()

    def messageListener(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.localProcInfo['procAddr']))
        while True:
            self.messageHandler(s.recv(BUFSIZE))

    def messageSender(self, address, msg):
        message = bytes(msg, 'UTF-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(address)
        s.send(message)
        s.close()

    def messageHandler(self, msg):
        recvdMessage = json.loads(msg)

        if recvdMessage['type'] == REQUEST:
            if self.localProcInfo['procTimestamp'] == None:
                msg = json.dumps({'type': REPLY, 'procInfo': self.localProcInfo})
                self.messageSender(tuple(recvdMessage['procInfo']['procAddr']), msg)
            elif((recvdMessage['procInfo']['procTimestamp'] > self.localProcInfo['procTimestamp']) and (self.localProcInfo['procState'] == WANTED)):
                self.defferedQueue.append(recvdMessage['procInfo']['procAddr'])
        elif recvdMessage['type'] == REPLY:
            if len(self.replyQueue) == 0:
                pass
            else:
                self.replyQueue.remove(tuple(recvdMessage['procInfo']['procAddr']))
        else:
            print("Something got fucked up")

    def MutexLock(self, mutex):
        self.localProcInfo['procState'] = WANTED
        self.localProcInfo['procTimestamp'] = time.time()
        requestMessage = json.dumps({'type': REQUEST, 'procInfo': self.localProcInfo, 'mutex': mutex})
        for address in self.remoteAddresses.values():
            self.messageSender(address, requestMessage)
            self.replyQueue.append(address)
        while len(self.replyQueue) > 0: pass
        return True

    def MutexRelease(self, mutex):
        self.localProcInfo['procState'] = RELEASED
        self.localProcInfo['procTimestamp'] = None
        replyMessage = json.dumps({'type': REPLY, 'procInfo': self.localProcInfo, 'mutex': mutex})
        for address in self.remoteAddresses.values():
            self.messageSender(address, replyMessage)
            #self.defferedQueue.remove(address)
        return True
        
    def MutexExit(self):
        os.system("taskkill %d"%(os.getppid()))
        return True