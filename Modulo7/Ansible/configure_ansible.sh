#!/bin/bash

# Author: Stefano Pilla - me [at] stefanopilla.it

echo "##############"
echo "Update repositories and install Ansible"
echo "##############"

# Update repositories
sudo apt-get update

# Install Python3 pip and sshpass
sudo apt-get install python3-pip sshpass -y

# Install Ansible
sudo pip3 install ansible

# Install Paramiko
sudo pip3 install paramiko

# Verify Ansible version
ansible --version

echo "##############"
echo "Creating project folder structure "
echo "##############"

# Create an Ansible project folder 
mkdir ansible_test
cd ansible_test

echo "DONE!"
echo " "

echo "##############"
echo "Creating Ansible Configuration file "
echo "##############"
# Create a default configuration file
touch ansible.cfg

# Default values
echo "[defaults]" >> ansible.cfg
# To gather fact you'll need to explicit declare it
echo "gathering = explicit" >> ansible.cfg
# Set the inventory filename, this option can be overridden with -i option
echo "inventory = inventory.ini" >> ansible.cfg
# Do not show deprecation warnings
echo "deprecation_warnings = False" >> ansible.cfg
# Disable host key checks - Activate it in production
echo "host_key_checking = False" >> ansible.cfg


echo "DONE!"
echo " "

echo "##############"
echo "Creating Ansible Inventory file "
echo "##############"

# Create inventory.ini file 
touch inventory.ini
echo "[ios_routers]" >> inventory.ini
echo "10.99.99.240" >> inventory.ini
echo "10.99.99.241" >> inventory.ini
echo " " >> inventory.ini
echo "[ios_switches]" >> inventory.ini
echo "10.99.99.244" >> inventory.ini

echo "DONE!"
echo " "

echo "##############"
echo "Creating Group and Host vars folders"
echo "##############"

# Define group variables
mkdir group_vars
cd group_vars

# Create ios_routers file for the variables related
# to this group
touch ios_routers

echo "---" >> ios_routers
echo "ansible_connection: network_cli" >> ios_routers
echo "ansible_network_os: ios" >> ios_routers

touch ios_switches

echo "---" >> ios_switches
echo "ansible_connection: network_cli" >> ios_switches
echo "ansible_network_os: ios" >> ios_switches

# Create host specific variables files 
cd .. && mkdir host_vars && cd host_vars
touch 10.99.99.240.yml
touch 10.99.99.241.yml
touch 10.99.99.244.yml

echo "############## Defining 10.99.99.240 vars ... ##############"

# Create variables for 10.99.99.240 - Router
echo "---" >> 10.99.99.240.yml
echo 'ansible_user: "cisco"' >> 10.99.99.240.yml
echo 'ansible_password: "cisco"' >> 10.99.99.240.yml
echo 'ansible_network_os: "ios"' >> 10.99.99.240.yml
echo 'ip_int_l0: 192.168.1.1' >> 10.99.99.240.yml
echo 'ip_int_l1: 192.168.1.129' >> 10.99.99.240.yml

echo "############## Defining 10.99.99.241 vars ... ##############"
# Create variables for 10.99.99.241 - Router
echo "---" >> 10.99.99.241.yml
echo 'ansible_user: "cisco"' >> 10.99.99.241.yml
echo 'ansible_password: "cisco"' >> 10.99.99.241.yml
echo 'ansible_network_os: "ios"' >> 10.99.99.241.yml
echo 'ip_int_l0: 192.168.2.1' >> 10.99.99.241.yml
echo 'ip_int_l1: 192.168.2.129' >> 10.99.99.241.yml

echo "############## Defining 10.99.99.244 vars ... ##############"
# Create variables for 10.99.99.244 - Switch
echo "---" >> 10.99.99.244.yml
echo 'ansible_user: "cisco_user"' >> 10.99.99.244.yml
echo 'ansible_password: "ciscopass"' >> 10.99.99.244.yml
echo 'ansible_network_os: "ios"' >> 10.99.99.244.yml

echo "DONE!"
echo " "

cd ..
# Test Connectivity
echo "##############"
echo "Testing Connectivity with hosts..."
echo "##############"
ansible -m ping ios_routers
ansible -m ping ios_switches

cd ..
# Copy the playbooks into the ansible main folder
cp configure_routers.yml ansible_test/
cp configure_switches.yml ansible_test/
cp clean_up_routers.yml ansible_test/
cp clean_up_switches.yml ansible_test/
cp -r vars/ ansible_test/

cd ansible_test

echo "##############"
echo "Cleaning Up existing configurations..."
echo "##############"

ansible-playbook clean_up_routers.yml clean_up_switches.yml

echo "DONE!"
echo " "

echo "##############"
echo "Configuring Routers..."
echo "##############"

ansible-playbook configure_routers.yml

echo "##############"
echo "Configuring Switches..."
echo "##############"

ansible-playbook configure_switches.yml
