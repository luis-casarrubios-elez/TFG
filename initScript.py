#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, subprocess, time
from subprocess import call

#Primero, desde el directorio donde tengamos el “Dockerfile” ejecutamos lo siguiente:

os.system('sudo docker build -t upm/ats-ubuntu .')

#Creamos un bridge ovs

os.system('sudo ovs-vsctl add-br ovsNet')

#Ahora para correr un contenedor con la imagen generada (upm/ats-ubuntu) ejecutamos lo siguiente:

os.system('sudo docker run --privileged -i -t --name ats-ubuntu -d upm/ats-ubuntu')

#Conectamos nuestro contenedor al brigde creado y asignamos una interfaz y una dirección IP al mismo, para poder integrarlo en cualquier escenario o acceder desde el host:

os.system('sudo ovs-docker add-port ovsNet veth0 ats-ubuntu')

os.system('sudo docker exec -i -t ats-ubuntu /sbin/ifconfig veth0 10.2.0.1/24')

#Tendremos ahora un contenedor corriendo con el nombre “ats-ubuntu” en el que está instalado traffic server, listo para configurarse. Una posible configuración para usarlo como Forward Proxy Cache sería la siguiente:

os.system('sudo docker exec -i -t ats-ubuntu service trafficserver start')
time.sleep(5)
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i \'1 i\map http://10.2.0.1:8080/myCI/ http://{cache}\' /etc/trafficserver/remap.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i \'s/trafficserver 256M/trafficserver 2G/g\' /etc/trafficserver/storage.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i \'s/proxy.config.http.cache.required_headers INT 2/proxy.config.http.cache.required_headers INT 0/g\' /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i \'s/proxy.config.http.push_method_enabled INT 0/proxy.config.http.push_method_enabled INT 1/g\' /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i \'s/proxy.config.http.cache.when_to_revalidate INT 0/proxy.config.http.cache.when_to_revalidate INT 3/g\' /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i \'s/proxy.config.url_remap.remap_required INT 1/proxy.config.url_remap.remap_required INT 0/g\' /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i \'s/proxy.config.reverse_proxy.enabled INT 1/proxy.config.reverse_proxy.enabled INT 0/g\' /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i -e "\$aCONFIG proxy.config.http_ui_enabled INT 1" /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i -e "\$aCONFIG proxy.config.http.cache.ignore_client_no_cache INT 1" /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i -e "\$aCONFIG proxy.config.http.cache.ims_on_client_no_cache INT 0" /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu /bin/sed -i -e "\$aCONFIG proxy.config.http.cache.ignore_server_no_cache INT 1" /etc/trafficserver/records.config')
os.system('sudo docker exec -i -t ats-ubuntu service trafficserver restart')