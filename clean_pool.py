# clean the ip allocation from pool after container intergration testing 

import requests,json,base64,paramiko,pdb,yaml,os

mgr="192.168.0.66"
mgruser="admin"
mgrpasswd="Nicira123$"
cred=base64.b64encode('%s:%s'%(mgruser,mgrpasswd))
header={"Authorization":"Basic %s"%cred,"Content-type":"application/json"}

poolid=raw_input("input ip pool uuid: ")

# get ip pool allocation info
ep="/api/v1/pools/ip-pools/%s/allocations"%poolid
url="https://"+str(mgr)+str(ep)
conn=requests.get(url,verify=False,headers=header)
result=json.loads(conn.text).get('results')
try:
    for x in result:
        ip=x.get('allocation_id')
        del x["_protection"]
        body=json.dumps(x)
        ep1="/api/v1/pools/ip-pools/%s"%poolid+str('?action=RELEASE')
        url="https://"+str(mgr)+str(ep1)
        conn=requests.post(url,verify=False,headers=header,data=body)
        print conn.status_code
except TypeError:
    print "\n"
    print "there is no ip allocated in this pool"
    print "\n"    

