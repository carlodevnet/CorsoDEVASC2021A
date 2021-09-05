from netmiko import ConnectHandler

# Create a connectioHangder object to represent the ssh cli session
sshCli = ConnectHandler(
    device_type='cisco_ios',
    host='10.99.99.231',
    port=22,
    username="cisco",
    password="cisco",
)

# send some simple "exec" commands and display the returned output
print("Sending 'sh ip int brief'.")
output = sshCli.send_command("show ip int brief")
print(f"IP interface status and configuration: \n {output} \n")