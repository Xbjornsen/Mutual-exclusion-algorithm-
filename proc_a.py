#!/usr/bin/env python
from ricart_agrawala import Ricart_Agrawala
import time
import sys


nodeA = Ricart_Agrawala()
nodeA.node_init(('127.0.0.1',5551), 2, (('127.0.0.1',5552),('127.0.0.1',5553)))
nodeA.MutexLock('Mutex')
print('proc_a')
time.sleep(2)
nodeA.MutexRelease('Mutex')
time.sleep(10)
nodeA.MutexExit()

# def proc_a(nodeA):
#     nodeA.MutexLock('Mutex')
#     print('proc_a',time.time())
#     time.sleep(2)
#     nodeA.MutexRelease('Mutex')
#     time.sleep(10)
