#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, subprocess, time
from subprocess import call

#Eliminamos la interfaz del bridge ovs
os.system('sudo ovs-docker del-port ovsNet veth0 ats-ubuntu')

#Paramos el contenedor
os.system('sudo docker stop ats-ubuntu') 

#Eliminamos el contenedor
os.system('sudo docker rm ats-ubuntu')

#Eliminamos el bridge ovs
os.system('sudo ovs-vsctl del-br ovsNet')