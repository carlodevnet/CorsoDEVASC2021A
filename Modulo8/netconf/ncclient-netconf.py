from os import write
from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="10.99.99.231",
    port=830,
    username="cisco",
    password="cisco",
    hostkey_verify=False
)

print("#Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability) 


#netconf_reply = m.get_config(source="running")

#with open("output.xml", "a") as f:
#    f.write(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())