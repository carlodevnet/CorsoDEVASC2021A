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


netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <hostname>CSR_NETCONF</hostname>
  </native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_hostname)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
