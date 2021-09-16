import json
import time
import os
from DNAC_Requestor import DNACRequester
import logging

# logging.basicConfig(level=logging.DEBUG)


def main():
    dnac = DNACRequester(host="10.10.20.85", username="admin",
                         password="Cisco1234!", verify=False)

    # Loop over each type of site object
    for body_type in ["area", "building", "floor"]:
        # Load  the JSON data into python objects
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dir_path}/site_data/{body_type}.json", "r") as handle:
            data = json.load(handle)

        # Declare some local variables and print the status message
        site = data['site'][body_type]
        name = f"{site['parentName']}/{site['name']}"
        print(f"Adding {body_type} object {name}")

        # Issue an HTTP Post request to create the site object
        add_resp = dnac._req("dna/intent/api/v1/site",
                             method="post", jsonbody=data)

        # Debugging statement to troubleshoot
        #print(json.dumps(add_resp.json(), indent=2))

        # Check the status grabbing the executionStatusUrl from the response
        status_url = add_resp.json()['executionStatusUrl']
        # print(status_url)
        status_resp = wait_for_site_creation(dnac, status_url[1:])
        # print(status_resp.text)

        # Ensure that the creation is succeded, always return a succeful HTTP status code
        if status_resp.json()['status'].lower() != "success":
            raise ValueError("Site Object addition failed")
        else:
            print("*" * 50)
            print(f"{body_type} {name} successfully created!")
            print("*" * 50)

        # Get the object just created so we can optionally print it out
        get_resp = dnac._req("dna/intent/api/v1/site", params={"name": name})
        obj_data = get_resp.json()['response'][0]

        # Debugging statement to troubleshoot
        #print(json.dumps(get_resp.json(), indent=2))

        if body_type == "floor":
            floor_id = obj_data['id']
            print(f"Object created with id {floor_id}")

    # Load in dummy device body from JSON File
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{dir_path}/site_data/device.json", "r") as handle:
        data = json.load(handle)

    print()
    # Issue an HTTP request to add dummy device
    add_dev_resp = dnac._req(
        "dna/intent/api/v1/network-device", method="post", jsonbody=data)

    # Optionally print out the json for troubleshooting
    #print(json.dumps(add_dev_resp.json(), indent=2))

    # Need to wait to the device creation to be completed
    dnac._wait_for_task(add_dev_resp.json()[
                        'response']['taskId'])

    # Assign the new device to the floor

    new_ip = data['ipAddress'][0]
    assign_dev_resp = dnac._req(
        f"dna/system/api/v1/site/{floor_id}/device", method="post", jsonbody={"device": [{"ip": new_ip}]})

    # Wait for the device to be assigned to the floor
    status_url = assign_dev_resp.json()["executionStatusUrl"]
    status_resp = wait_for_site_creation(dnac, status_url[1:])

    # Confirm that the
    mem_resp = dnac._req(f"dna/intent/api/v1/membership/{floor_id}")

    # Print the membership response for debugging
    #print(json.dumps(mem_resp.json(), indent=2))

    # Perform a quick sanity check to ensure that the IP Address match the IP specified in the post request
    added_ip = mem_resp.json(
    )['device'][0]['response'][0]['managementIpAddress']
    if new_ip != added_ip:
        raise ValueError(f"IP Address don't match: {new_ip} != {added_ip}")

    # Print final status message
    print(f"Assigned device to floor {floor_id} with IP Address {new_ip}")


def wait_for_site_creation(dnac, status_url, wait_time=5):
    # Helper function to check the statu of the
    done = False
    while not done:
        time.sleep(wait_time)

        # After waiting 5 seconds, issue a get request to check the status
        status_resp = dnac._req(status_url)
        done = status_resp.json()['status'].lower() != "in_progress"

    return status_resp


if __name__ == "__main__":
    main()
