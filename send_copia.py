#!/usr/bin/env python

import sys,os
HOME=os.getenv("HOME")
sys.path.append('/%s/seiscomp3/share/gds/tools/' %HOME)

from lib import bulletin, logger, spooler
import subprocess
import json
import time
from datetime import datetime 

class copiaConfig:
    def __init__(self,config):

        prefix = "origen"
        try:  self.eqeventsFolder = config.get(prefix, "eqeventsFolder")
        except: self.eqeventsFolder="~/seiscomp3/var/lib/eqevents/pages/"
        try:  self.serverFile = config.get(prefix, "serverFile")
        except: self.eqeventsFolder=None
class SpoolCopia(spooler.Spooler):

    def __init__(self):

        spooler.Spooler.__init__(self)
        self._copia=copiaConfig(self._config)
        logger.info("##Cargado el origen %s" %self._copia)

    def _readServerFile(self,json_file):
        try:
            print(json_file)
            with open(json_file) as json_data_files:
                return json.load(json_data_files)
        except Exception, e:
            raise Exception("##Error in _readServerFile(): %s" %str(e))

    def spool(self,addresses,content):
        
        #print("##%" %addresses)
        """
        #self.eqeventsFolder="~/seiscomp3/var/lib/eqevents/pages/"
        #eqeventsFolder="/home/seiscomp/seiscomp3/var/lib/eqevents/pages/"
        $SEISCOMP3/var/lib/eqevents/
                            pages/
                                index.html*
                                events/
                                    igepn2018xxxa*/
                                    igepn2018xxxb/
                                browser*/
                                static/
                            spool
        """
        
        srvs=self._readServerFile(self._copia.serverFile)
        time.sleep(10)
        for a in addresses:
            srv=a[1]
            eventFolder='%s/events/%s' %(self._copia.eqeventsFolder,content.strip())
            pagesFolder='%s/' %(self._copia.eqeventsFolder)
            y=content.strip()[5:-4]
            browserFolder='%s/browser/' %(self._copia.eqeventsFolder)
            
            """La carpeta destino debe reflejara el contenido de PAGES"""
            destino='%s@%s:%s' %(srvs[srv]['username'],srvs[srv]['ip'],srvs[srv]['destino'])

            try:
                
                """"Copy the event folder"""
                logger.info('#Copiando evento %s a: %s/events/' %(content.strip(), destino) )
                subprocess.call(['sshpass -p `cat %s` scp -pr %s  %s/events/ ' %(srvs[srv]['password'],eventFolder, destino) ],shell=True)
                logger.info("Evento %s copiado " %(content.strip()))
                
                """ Copy the index.html file """
                logger.info('#Copiando index.html a: %s/' %( destino) )
                subprocess.call(['sshpass -p `cat %s` scp -pr %s/index.html %s/' %(srvs[srv]['password'],pagesFolder, destino) ],shell=True)
                logger.info("index.html copiado ")               
                
                """Copy the browser pages"""
                logger.info('#Copiando archivos browser a: %s' %(destino))
                subprocess.call(['sshpass -p `cat %s` scp -pr %s/%s*  %s/browser/ ' %(srvs[srv]['password'],browserFolder,y, destino) ],shell=True)
                logger.info("Carpeta browser copiado")
            except Exception as e:
                raise Exception("##No se pudo copiar a la carpeta %s: %s" %(destino,str(e)))


if __name__=="__main__":
    app=SpoolCopia()
    app()

