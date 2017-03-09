'''
Created on Mar 7, 2017

@author: wacero
'''

import sys
#Modify the path for own/external libraries
#sys.path.append('/home/igepn/plugins_python/copiaServidorWeb/')
import os 
import json
import logging
import configPlugin
import subprocess

logging.basicConfig(filename=os.path.join(configPlugin.log_dir, "copiaServidorWeb.log"), level=logging.DEBUG)
server_file = configPlugin.server_file

def read_config_file(json_file):
    '''
    Lee un archivo json y devuelve su contenido 
    como un diccionario de python 
    '''
    try:
        with open(json_file) as json_data_files:
            return json.load(json_data_files)
    except Exception as e:
        logging.debug("Error readConfigFile(): %s" % str(e))
        return -1


def copy_files(srvRmt):
    '''
    Copiar los archivos events*
    '''
    
    files_orig='%s/events*' %(configPlugin.www_dir)
    dest='%s@%s:%s' %(srvRmt['username'], srvRmt['ip'],srvRmt['destino'])
    try:
        subprocess.call('scp -pr %s %s' %(files_orig,dest),shell=True)
        logging.debug("copy_files() OK" ) 
        return 0
    except Exception as e:
        logging.debug("Error while copying files: %s" % (str(e))) 
        return -1
        

        
def copy_folder(evID, srvRmt):
    ''' 
    Copiar  la carpeta del evento
    '''
    event_orig = '%s/event/%s' % (configPlugin.www_dir, evID)
    event_dest = '%s@%s:%s/event/' % (srvRmt['username'], srvRmt['ip'],srvRmt['destino'])
    try:

        #logging.debug(event_dest,event_orig)
        subprocess.call(['scp','-pr',event_orig, event_dest])
        logging.debug("copy_folder() OK")
        return 0
    except Exception as e:
        logging.debug("Error while copying folder: %s" % (str(e))) 
        return -1



def principal(evID,server_name):

    servers = read_config_file(server_file)
    if servers == -1:
        logging.debug('Error while reading servers file: %s' % (server_file))
        return -1
    else:
        logging.debug("Read json file ok")
    
    '''
    client = connect2server(servers[configPlugin.server_name])
    if client == -1:
        logging.debug("Error connect2server(). Exit")
        return -1
    else:
        logging.debug("connect2server() ok")
    '''    
    
    if copy_files(servers[server_name]) == 0 and copy_folder(evID,servers[server_name]) ==0:
        return "Files copied ok, copiaServidorWeb_plugin exit"
    else:
        return "Something went wrong, check copiaServidorWeb.log, copiaServidorWeb_plugin exit"


#print principal('igepn2017aksy','srvTest1')

#print principal('igepn2017aksy','srvTest2')





    
    
    
    
    
    
