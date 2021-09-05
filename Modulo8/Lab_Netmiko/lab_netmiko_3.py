from netmiko import ConnectHandler

# Create a connectioHangder object to represent the ssh cli session
sshCli = ConnectHandler(
    device_type='cisco_ios',
    host='10.99.99.231',
    port=22,
    username="cisco",
    password="cisco",
)

output = sshCli.send_command("show ip int brief")
print(f"IP interface status and configuration: \n {output} \n")

config_commands = [
    'int loopback 1',
    'ip address 2.2.2.2 255.255.255.0',
    'description Configured via Netmiko'
]

output = sshCli.send_config_set(config_commands)
print(f"Config output from the device: \n {output} \n")

output = sshCli.send_command("show ip int brief")
print(f"IP interface status and configuration: \n {output} \n")

config_commands = [
    'int loopback 2',
    'ip address 2.2.2.2 255.255.255.0',
    'description Configured via Netmiko'
]

output = sshCli.send_config_set(config_commands)
print(f"Config output from the device: \n {output} \n")

output = sshCli.send_command("show ip int brief")
print(f"IP interface status and configuration: \n {output} \n")