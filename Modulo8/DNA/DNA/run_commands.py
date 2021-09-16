import os
import requests
from DNAC_Requestor import DNACRequester
import json


def main():

    dnac = DNACRequester(host="10.10.20.85", username="admin",
                         password="Cisco1234!", verify=False)

    # Define the list of devices on which we want to run commands
    # In this case we select all the Switches and Hubs Cisco Catalyst 9300 Series
    search_params = {
        "family": "Switches and Hubs",
        "type": "Cisco Catalyst 9300 Switch"
    }

    # We create a request with the helper functions
    devices = dnac._req("dna/intent/api/v1/network-device",
                        params=search_params)

    #print(json.dumps(devices.json(), indent=2))
    # Create an empty list to store uuids of the devices
    device_uuids = []

    # Iterare through the response
    for device in devices.json()['response']:
        # If there are no errors add it to the list otherwise ignore the devices
        if not device['errorCode']:
            print(f"Adding {device['hostname']} : {device['instanceUuid']}")
            device_uuids.append(device['instanceUuid'])
        else:
            print(f"An Error occured so I'm ignoring the device....")

    # Create a dict of commands to run
    commands_body = {
        "commands": ["show inventory", "show version", "show badstuff"],
        "deviceUuids": device_uuids
    }

    # Create a request using helper functions to run these commands
    resp_task = dnac._req("dna/intent/api/v1/network-device-poller/cli/read-request",
                          method="post", jsonbody=commands_body).json()
    # Aynch so we ll wait for the response
    resp_status = dnac._wait_for_task(resp_task['response']['taskId'])

    #print(json.dumps(resp_status.json(), indent=2))

    # Get the results and grab the "fileId" field that we will use later
    fileId = json.loads(resp_status.json()['response']['progress'])['fileId']

    # Create a requests issuing a get requests to download a file with the result of the commands
    file_resp = dnac._req(f"dna/intent/api/v1/file/{fileId}")

    # Create folders and file to store the results locally
    file_dir = "cmd_outputs"
    dirpath = os.path.dirname(__file__)
    if not os.path.exists(f"{dirpath}/{file_dir}"):
        os.makedirs(f"{dirpath}/{file_dir}")

    # Iterare throught the file and grab the deviceUuid then use it to create the file name and write the output of the command
    for item in file_resp.json():
        uuid = item['deviceUuid']
        for result, cmd_dict in item['commandResponses'].items():
            for cmd, output in cmd_dict.items():
                print(f"{uuid} : {cmd} --> {result}")
            cmd_u = cmd.replace(" ", "_")
            with open(f"{dirpath}/{file_dir}/{uuid}_{cmd_u}.txt", "w") as handle:
                handle.write(output)


if __name__ == "__main__":
    main()
