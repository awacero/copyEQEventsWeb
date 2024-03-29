This repository contains code of a GDS plugin to copy the eqevents web pages to a list of servers. 

The configuration files used are: 

        send_copia.cfg: information used by filter_copia.py and send_copia.py
        servidores.json: information of the servers where the eqevents folders are copied to. 
     
# Configure in GDS
## Front End
Add the service in GDS web page as shown in the next figure
![Service config example](https://github.com/awacero/copiaServidorWeb/raw/master/img/gds_copiaEvento.png)

## Back End

``` bash

#GDS Config file: $HOME/seiscomp3/etc/gds.cfg 

service.copiaEvento.directory = ${HOME}/plugins_python/copiaServidorWeb
service.copiaEvento.filter.primary.cmd = ${HOME}/plugins_python/copiaServidorWeb/filter_copia.py
service.copiaEvento.spooler.cmd = ${HOME}/plugins_python/copiaServidorWeb/send_copia.py
service.copiaEvento.spooler.timeout = 120

```

Restart the GDS daemon

```
$ seiscomp restart gds 
```
