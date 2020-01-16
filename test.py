#!/usr/bin/env python
from ricart_agrawala import Ricart_Agrawala
import proc_a, proc_b, proc_c
import time
import sys
import threading


nodeA = Ricart_Agrawala()
nodeB = Ricart_Agrawala()
nodeC = Ricart_Agrawala()
nodeA.node_init(('127.0.0.1',5551), 2, (('127.0.0.1',5552),('127.0.0.1',5553)))
nodeB.node_init(('127.0.0.1',5552), 2, (('127.0.0.1',5551),('127.0.0.1',5553)))
nodeC.node_init(('127.0.0.1',5553), 2, (('127.0.0.1',5551),('127.0.0.1',5552)))

threadA = threading.Thread(target=proc_a.proc_a, args=(nodeA,))
threadB = threading.Thread(target=proc_b.proc_b, args=(nodeB,))
threadC = threading.Thread(target=proc_c.proc_c, args=(nodeC,))

threadB.start()
threadC.start()
threadA.start()