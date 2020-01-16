#!/usr/bin/env python
from ricart_agrawala import Ricart_Agrawala
import time
import sys


nodeB = Ricart_Agrawala()
nodeB.node_init(('127.0.0.1',5552), 2, (('127.0.0.1',5551),('127.0.0.1',5553)))
time.sleep(5)
nodeB.MutexLock('Mutex')
print('proc_b')
time.sleep(2)
nodeB.MutexRelease('Mutex')
time.sleep(10)
nodeB.MutexExit()

# def proc_b(nodeB):
#     time.sleep(5)
#     nodeB.MutexLock('Mutex')
#     print('proc_b',time.time())
#     time.sleep(2)
#     nodeB.MutexRelease('Mutex')
#     time.sleep(10)
