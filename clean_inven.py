# clean the inventory from kubernetes creation

import requests,json,base64,paramiko,pdb,yaml,os

mgr="192.168.0.66"
mgruser="admin"
mgrpasswd="Nicira123$"
cred=base64.b64encode('%s:%s'%(mgruser,mgrpasswd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}

print "this will delete t1 LR, lsw port, lsw,ip pool which refers oc/k8 cluster"
cluster=raw_input("input ip cluster nane: ")
print "this will delete all subnet allocation"
ip_block=raw_input("input ip block name: ")


## get t1 related to cluster 
ep="/api/v1/logical-routers?router_type=TIER1"
url="https://"+str(mgr)+str(ep)
conn=requests.get(url,verify=False,headers=header)
result=json.loads(conn.text).get('results')
t1r=[]
for x in result:
    if cluster in x.get('display_name'):
        uuid=x.get('id')
        t1r.append(uuid)
    elif t1r==[]:
       continue

# delete lrouters in t1r matrix
for x in t1r:
    ep="/api/v1/logical-routers/%s?force=True"%x
    url="https://"+str(mgr)+str(ep)
    conn=requests.delete(url,verify=False,headers=header)
    if conn.status_code!=200:
        print url+" is not deleted"
        print conn.text
    else: 
        continue

# get lsw port which refers oc cluster 
ep="/api/v1/logical-ports"
url="https://"+str(mgr)+str(ep)
conn=requests.get(url,verify=False,headers=header)
result=json.loads(conn.text).get('results')
lswport=[]
for x in result:
    if cluster in x.get('display_name'):
        uuid=x.get('id')
        lswport.append(uuid)
    elif lswport==[]:
        continue

# delete lswport which refers oc cluster 
for x in lswport:
    ep="/api/v1/logical-ports/%s?detach=True"%x
    url="https://"+str(mgr)+str(ep)
    conn=requests.delete(url,verify=False,headers=header)
    if conn.status_code!=200:
        print url+" is not deleted"
        print conn.text
    else:
        continue

# get lsw which refers oc cluster 
ep="/api/v1/logical-switches"
url="https://"+str(mgr)+str(ep)
conn=requests.get(url,verify=False,headers=header)
result=json.loads(conn.text).get('results')
lsw=[]
for x in result:
    if cluster in x.get('display_name'):
        uuid=x.get('id')
        lswport.append(uuid)
    elif lswport==[]:
        continue

# delete lsw which refers oc cluster 
for x in lswport:
    ep="/api/v1/logical-switches/%s?detach=True"%x
    url="https://"+str(mgr)+str(ep)
    conn=requests.delete(url,verify=False,headers=header)
    if conn.status_code!=200:
        print url+" is not deleted"
        print conn.text
    else:
        continue

# get ip pool which refers oc cluster 
ep="/api/v1/pools/ip-pools"
url="https://"+str(mgr)+str(ep)                                                                                         
conn=requests.get(url,verify=False,headers=header)                                                                      
result=json.loads(conn.text).get('results')                                                                             
pool=[]                                                                                                                  
for x in result:                                                                                                        
    if cluster in x.get('display_name'):                                                                                
        uuid=x.get('id')                                                                                                
        pool.append(uuid)                                                                                            
    elif pool==[]:
        continue                         

# delete ip pool which refers oc cluster 
for x in pool:                                                                                                       
    ep="/api/v1/pools/ip-pools/%s?force=True"%x                                                                      
    url="https://"+str(mgr)+str(ep)                                                                                     
    conn=requests.delete(url,verify=False,headers=header)                                                               
    if conn.status_code!=200:                                                                                           
        print url+" is not deleted"                                                                                     
        print conn.text                                                                                                 
    else:                                                                                                               
        continue             
