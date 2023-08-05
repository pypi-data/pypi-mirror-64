# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 3. 18..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from vvv_vra import *

SDK.VRA.system('https://vra.vmkloud.com', 'jangh', 'David*#8090')


def getDeployments():
    return [ dep.name for dep in Deployment.list() ]


def getAPVMs(deploy_name):
    vms = []
    for vm in Machine.list():
        prop = vm.customProperties
        if 'prjName' in prop and prop['prjName'] == deploy_name:
            if 'prjType' in prop and prop['prjType'] == 'app':
                for tag in vm.tags:
                    if tag['key'] == 'prjStat' and tag['value'] == 'infra-ready':
                        vms.append({
                            'name' : vm.name,
                            'ip' : vm.address
                        })
    return vms

def getDBVMs(deploy_name):
    vms = []
    for vm in Machine.list():
        prop = vm.customProperties
        if 'prjName' in prop and prop['prjName'] == deploy_name:
            if 'prjType' in prop and prop['prjType'] == 'db':
                for tag in vm.tags:
                    if tag['key'] == 'prjStat' and tag['value'] == 'infra-ready':
                        vms.append({
                            'name' : vm.name,
                            'ip' : vm.address
                        })
    return vms


print(getAPVMs('nh1'))
print(getDBVMs('nh2'))

# def getIPofVM(deployment_name, ):
# 
# vms = Machine.list()
# print(len(vms))
# for vm in vms:
#     if 'tags' in vm:
#         for tag in vm.tags:
#             if tag['key'] == 'prjDep' and tag['value'] == 'n1':
#                 print(vm)
        
