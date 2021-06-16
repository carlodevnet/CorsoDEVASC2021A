# Author: Stefano Pilla 

import json
import time
import os

# Import the libraries
from DNA_Requester import DNACRequester


def main():

    # Create a new DNA Object
    dnac = DNACRequester(host="10.10.20.85", username="admin",
                         password="Cisco1234!", verify=False)

    # Define a list for the credentials, this is a DNA requirement
    cred_list = []
    # Define a list for the credentails type, this is a DNA requirement
    cred_types = ["CLI", "SNMPV2_READ_COMMUNITY", "SNMPV2_WRITE_COMMUNITY"]

    # Let's iterate on those 2 lists to get the credentials configured in DNA
    for cred in cred_types:
        cred_resp = dnac._req(
            "dna/intent/api/v1/global-credential", params={"credentialSubType": cred})

    # Let's print the response with the credentials
    print(json.dumps(cred_resp.json(), indent=2))

    # We know that the the DevNet Sandbox has 1 for each cred_type. 
    # In a production env you sohuld be more specific.
    if cred_resp.json()['response'][0] == "":
        print(f"Credential List is empty!")
    else:
        # Get the id of the credentials from the converted (in json) response
        cred_id = cred_resp.json()['response'][0]['id']
        
        # Add the id to the list of the cred_list and print it
        cred_list.append(cred_id)
        print(f"Collected {cred} credential with ID {cred_id}")

        # Load in a list of dictionaries containing the discovery parameters
        # These are the data that we would like to pass to the DNA Center
        # to start with the discovery phase
        dirpath = os.path.dirname(__file__)
        with open(f"{dirpath}/site_data/discoveries.json", "r") as handle:
            discoveries = json.load(handle)

        # Loop over each discovery in the disctionary and update the dict with the cred list and run the discovery
        for disc_body in discoveries:
            disc_body['globalCredentialIdList'] = cred_list
            run_discovery(dnac, disc_body)


# Create a method and pass the discovery that we would like to run (disc_body)
def run_discovery(dnac, disc_body, timeout=600):
 
    # Given an existing DNA object on which we will run discoveries based on the disc_body dict. 
    # This function perfoms
    # 1. Create a new discovery
    # 2. Waits specificed timeout for discovery to complete (default 10min)
    # 3. Create discovered_devices/ directory with subdirs for each discovery

    # Create a new request with disc_body as payload
    disc_resp = dnac._req("dna/intent/api/v1/discovery",
                          method="post", jsonbody=disc_body)

    # DNA will respond with a taskId that we will use to keep track of the status with our helper function
    disc_task = dnac._wait_for_task(disc_resp.json()['response']['taskId'])

    # Once completed we can get the discovery id and check the progress
    disc_id = disc_task.json()['response']['progress']

    # Let's check if the discovery was successful
    success = False

    # Iterate through 0 to the 600 floor division of 10 so we are just counting from 0 to 59
    for i in range(timeout // 10):
        # get the status of the discovery
        get_disc = dnac._req(f"dna/intent/api/v1/discovery/{disc_id}")
        # record the response
        data = get_disc.json()['response']
        # print(data)
        # if not completed, print the current status
        # we use .lower() to make sure we won't have case-sensitive issues
        if data['discoveryCondition'].lower() != "complete":
            print(f"Discovery {disc_id} {data['discoveryCondition']} {i}")
            # Is it's not complete, wait for 10 second before the next iteration
            time.sleep(10)

        # If the task is complete so data['discoveryCondition'].lower() == "complete"
        # Get the discovered devices and change the status value to "True"
        else:
            print(f"Discovery {disc_id} found {data['numDevices']} devices")
            success = True
            break

    # If the for loop didn't set the Success variable to True is means that has not finished and taht the timeout is expired
    if not success:
        raise TimeoutError("The discovery didn't complete in time!")

    # If completed then we can create files with the results
    # Get the directory where the file is executed
    dirpath = os.path.dirname(__file__)

    #Create a variable to store the complete path with the discovery id (disc_id)
    file_dir = f"{dirpath}/disc_output/{disc_id}"

    # If the directory doesn't exist, let's create it
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # Get a list of the discovered devices and their status from DNA Center 
    # and store the value into dev_sum variable
    dev_sum = dnac._req(
        f"dna/intent/api/v1/discovery/{disc_id}/network-device")

    # Iterate through the discovered devices from the "reponse" key
    for dev in dev_sum.json()['response']:

        # if the device were reachable via CLI or SNMP
        if dev['reachabilityStatus'].lower() == "success":
            print(f"{dev['hostname']} was reachable")

        # ...and they are already in the system as managed devices
        # let's get all the details from DNA with a new request
        if dev['inventoryReachabilityStatus'].lower() == "reachable":
            get_dev = dnac._req(
                f"dna/intent/api/v1/network-device/{dev['id']}")

            # Create a top-level dict with "discovery" and "device" keys
            # where we can store all the info for the discovery and for the device
            output = {"discovery": dev, "device": get_dev.json()['response']}

            # Create the json file with all the info of the discovered device
            with open(f"{file_dir}/{dev['hostname']}.json", "w") as handle:
                json.dump(output, handle, indent=2)

        # Else, discovered failed so print the device IP address and reason
        else:
            print(
                f"Device {dev['managementIpAddress']}"
                f"failed: {dev['reachabilityFailureReason']}"
            )


if __name__ == "__main__":
    main()
