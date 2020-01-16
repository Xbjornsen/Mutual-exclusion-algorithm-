#!/usr/bin/env python
from ricart_agrawala import Ricart_Agrawala
import time
import sys

nodeC = Ricart_Agrawala()
nodeC.node_init(('127.0.0.1',5553), 2, (('127.0.0.1',5551),('127.0.0.1',5552)))
time.sleep(6)
nodeC.MutexLock('Mutex')
print('proc_c')
time.sleep(2)
nodeC.MutexRelease('Mutex')
time.sleep(10)
nodeC.MutexExit()

# def proc_c(nodeC):
#     time.sleep(6)
#     nodeC.MutexLock('Mutex')
#     print('proc_c',time.time())
#     time.sleep(2)
#     nodeC.MutexRelease('Mutex')
#     time.sleep(10)