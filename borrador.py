'''
Created on Mar 7, 2017

@author: wacero
'''


    
def lista_events():
    lista=['events.html']
    for i in range(1,25):
        #print()
        lista.append("events%s.html" %(i))
    
    return lista 
        


import subprocess
origen="/home/seiscomp/seiscomp3/var/lib/eqevents/www/event/igepn2017brca"
host="wacero@192.168.1.118"
destino="/home/wacero/"

subprocess.call(['scp','-pr',origen,'%s:%s' %(host,destino)])
