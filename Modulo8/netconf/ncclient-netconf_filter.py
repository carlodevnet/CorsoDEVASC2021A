from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="10.99.99.231",
    port=830,
    username="cisco",
    password="cisco",
    hostkey_verify=False
)

'''
print("#Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability) 
'''

netconf_filter = open("filter.xml").read()

print(netconf_filter)

netconf_reply = m.get_config(source="running", filter=("subtree", netconf_filter))
print(netconf_reply)
