# the script is to migrate vsphere vss vmk interface to NSX-T N-VDS 

import requests,json,base64,time

mgr="192.168.110.201"
user="admin"
password="VMware1!"

# the vmk interface to be migrated 
vmkint="vmk1"
# the destination vswitch(nsx or vss PG) to migrate 
lswid="5efe8244-2de9-42c9-9c03-af84ea780fdd"
#lswid="VM Network"

cred=base64.b64encode('%s:%s'%(user,password))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}

def get_esxnode():
    ep="/api/v1/fabric/nodes?resource_type=HostNode"
    url="https://"+str(mgr)+str(ep)
    conn=requests.get(url,verify=False,headers=header)
    return conn.text

def get_tnbody(uuid):
    ep="/api/v1/transport-nodes/%s"%(uuid)
    url="https://"+str(mgr)+str(ep)
    conn=requests.get(url,verify=False,headers=header)
    return conn.text

def put_migratevmk(tnuuid,body):
    ep="/api/v1/transport-nodes/%s?if_id=%s&esx_mgmt_if_migration_dest=%s"%(tnuuid,vmkint,lswid)
    url="https://"+str(mgr)+str(ep)
    body=body
    conn=requests.put(url,verify=False,headers=header,data=body)
    return conn.text

# get host type equal to ESX
esxnode=json.loads(get_esxnode()).get('results')

matrix=[]

for x in esxnode:

    if x.get('os_type') == "ESXI":
        uuid=x.get('id')
        matrix.append(uuid)
    else:
        pass

# use esx host uuid to retrieve returned body and delete unnecessary dict
# then update back 
for y in matrix:
    body=json.loads(get_tnbody(y))
    del body["_create_user"]
    del body["_create_time"]
    del body["_last_modified_user"]
    del body["_last_modified_time"]
    del body["_system_owned"]
    del body["_protection"]
    newbody=json.dumps(body)
    print put_migratevmk(y,newbody)  # vmk migration functon call 
    time.sleep(2)
