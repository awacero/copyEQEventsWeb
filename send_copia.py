#!/usr/bin/env seiscomp-python 

import sys,os

sys.path.append( os.path.join(os.environ['SEISCOMP_ROOT'],'share/gds/tools/'))

from lib import bulletin, spooler
import subprocess
from subprocess import Popen, PIPE, STDOUT
import json
import time
from datetime import datetime 


import logging
import logging.config

logging_file = os.path.join(os.environ['SEISCOMP_ROOT'],'var/log/','gds_service_copiaEvento.log')
logging.basicConfig(filename=logging_file, format='%(asctime)s %(message)s')
logger = logging.getLogger("copiaEvento")
logger.setLevel(logging.DEBUG)

class copiaConfig:
    def __init__(self,config):

        prefix = "eqevents"
        try:  
            self.eqevents_path = config.get(prefix, "eqevents_path")
        except Exception as e: 
            logger.error("Error reading cfg file: %s" %e)
            self.eqevents_path="~/seiscomp/var/lib/eqevents/pages/"
        try:  
            self.target_server_file = config.get(prefix, "target_server_file")
        except: 
            self.target_server_file=None

class SpoolCopia(spooler.Spooler):

    def __init__(self):
        spooler.Spooler.__init__(self)
        self._copia=copiaConfig(self._config)
        
    def _readServerFile(self,json_file):
        try:
            with open(json_file) as json_data_files:
                return json.load(json_data_files)
        except Exception as e:
            raise Exception("##Error in _readServerFile(): %s" %str(e))

    def spool(self,addresses,content):
        

        """From events folder, just the event folder must be copied
           From browser just the last year must be copied"""
        """
        EQEVENTS folder structure
        $SEISCOMP_ROOT/var/lib/eqevents/
                            pages/
                                index.html*
                                events/
                                    igepn2018xxxa*/
                                    igepn2018xxxb/
                                browser/*
                                browser.html *
                                static/
                            spool
        """
        event_folder = '%s/events/%s' %(self._copia.eqevents_path,content.strip())
        pages_folder='%s/' %(self._copia.eqevents_path)
        year = content.strip()[5:-4]
        browser_folder='%s/browser/' %(self._copia.eqevents_path)

        if not os.path.exists(event_folder):
            time.sleep(15)
        target=self._readServerFile(self._copia.target_server_file)
        
        for a in addresses:
            target_name=a[1]
            
            """La carpeta target_path debe reflejara el contenido de PAGES"""
            target_path='%s@%s:%s' %(target[target_name]['username'],target[target_name]['ip'],target[target_name]['target_path'])

            try:
                
                """"Copy the event folder"""
                logger.info('#Copying event %s to: %s/events/' %(content.strip(), target_path) )
                subprocess.call(['sshpass -p `cat %s` scp -pr %s  %s/events/ ' 
                                %(target[target_name]['password'],event_folder, target_path) ],shell=True)
                logger.info("Event %s copied " %(content.strip()))
                
            except Exception as e:
                logger.error("Could not copy %s: %s" %(target_path,str(e)))

            try:

                """ Copy the index.html file """
                logger.info('#Copying index.html a: %s/' %( target_path) )
                subprocess.call(['sshpass -p `cat %s` scp -pr %s/index.html %s/' 
                                %(target[target_name]['password'],pages_folder, target_path) ],shell=True)
                logger.info("index.html copied ")
            except Exception as e:
                logger.error("Could not copy %s: %s" %(target_path,str(e)))

            try:
                """ Copy the browser.html file """
                logger.info('#Copying browser.html a: %s/' %( target_path) )
                subprocess.call(['sshpass -p `cat %s` scp -pr %s/browser.html %s/' 
                                %(target[target_name]['password'],pages_folder, target_path) ],shell=True)
                logger.info("browser.html copied ")                
            except Exception as e:
                logger.error(" Could not copy %s: %s" %(target_path,str(e)))

            try:
                """ Copy the events.csv and events.xml files """
                logger.info('#Copying events.* a: %s/' %( target_path) )
                result = subprocess.check_output(['sshpass -p `cat %s` scp -pr %s/events.* %s/' 
                                                %(target[target_name]['password'],pages_folder, target_path) ],shell=True)
                logger.info("events.* copied: %s" %result)        
            except Exception as e:
                logger.error("Could not copy %s: %s" %(target_path,str(e)))
            try:
                """Copy the browser pages"""
                logger.info('#Copying browser to: %s' %(target_path))
                result = subprocess.check_output(['sshpass -p `cat %s` scp -pr %s/%s*  %s/browser/ ' 
                                                %(target[target_name]['password'],browser_folder,year, target_path) ],shell=True)
                logger.info("Folder browser copied: %s" %result)
            
            except Exception as e:
                logger.error("Could not copy %s: %s" %(target_path,str(e)))


if __name__=="__main__":
    app=SpoolCopia()
    app()

