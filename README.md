# copiaServidorWeb

##copiaServidorWeb_plugin.py
##Archivo principal que se encarga de la conexión con el computador y la copia de los archivos
##servidores.json
##Archivo con la información de USUARIO/CLAVE de cada servidor
##configPlugin.py
##Archivo de configuración con información de las carpetas, nombres de archivos, etc. 


##copiaServidorWeb.log
##Los mensajes de funcionamiento normal o error se almacenan en este archivo. 
##El script está configurado con un logging en modo DEBUG. 

El archivo de configuración de servidores.json tiene el siguiente formato

{
        "srvTest1":{
                "username":"usuario",
                "password":"claveusuario",
                "ip":"xxx.xxx.xxx.xxx",
                "port":xx,
                "destino":"/home/usuario/testcopiaremota",
                "timeout":"10"
        },
        "srvTest2":{
                "username":"usuario",
                "password":"claveusuario",
                "ip":"xxx.xxx.xxx.xxx",
                "port":xxx,
                "destino":"/home/usuario/testcopiaremota",
                "timeout":"10"
        },
        "srvCloud":{
                "username":"xxxx",
                "password":"xxxxxx",
                "ip":"xxx.xxx.xxx",
                "port":xxx,
                "destino":"/home/usuario/testcopiaremota",
                "timeout":"10"
        }

}
