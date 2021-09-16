import json
import time
import os
from DNAC_Requestor import DNACRequester


def main():

    dnac = DNACRequester(host="10.10.20.85", username="admin",
                         password="Cisco1234!", verify=False)

    cred_list = []
    cred_types = ["CLI", "SNMPV2_READ_COMMUNITY", "SNMPV2_WRITE_COMMUNITY"]

    for cred in cred_types:
        cred_resp = dnac._req(
            "dna/intent/api/v1/global-credential", params={"credentialSubType": cred})
    print(json.dumps(cred_resp.json(), indent=2))
    # The DevNet Sandbox has 1 for each cred_type. In a production env you sohuld be more specific.
    if cred_resp.json()['response'][0] == "":
        print(f"Credential List is empty!")
    else:
        cred_id = cred_resp.json()['response'][0]['id']
        print(cred_id)
        cred_list.append(cred_id)
        print(f"Collected {cred} credential with ID {cred_id}")

        # Load in a list of dictionaries containing the discvoery parameters
        dirpath = os.path.dirname(__file__)
        with open(f"{dirpath}/site_data/discoveries.json", "r") as handle:
            discoveries = json.load(handle)

        # Loop over each discovery in the disctionary and update the dict with the cred list and run the discovery
        for disc_body in discoveries:
            disc_body['globalCredentialIdList'] = cred_list
            run_discovery(dnac, disc_body)


def run_discovery(dnac, disc_body, timeout=600):
    # Give an existing dna object and a discovery payload, this function perfoms
    # 1. Create a new discovery
    # 2. Waits specificed timeour for discovery to complete (default 10min)
    # 3. Create discovered_devices/ directory with subdirs for each discovery

    # Create a new request with disc_body as payload
    disc_resp = dnac._req("dna/intent/api/v1/discovery",
                          method="post", jsonbody=disc_body)

    # DNA will respond with a taskId that we will use to keep track of the status with our helper function
    disc_task = dnac._wait_for_task(disc_resp.json()['response']['taskId'])

    # Once completed we can get the discovery id
    disc_id = disc_task.json()['response']['progress']

    success = False
    for i in range(timeout // 10):
        get_disc = dnac._req(f"dna/intent/api/v1/discovery/{disc_id}")
        data = get_disc.json()['response']

        # if not completed, print the current status
        if data['discoveryCondition'].lower() != "complete":
            print(f"Discovery {disc_id} {data['discoveryCondition']} {i}")
            time.sleep(10)

        else:
            print(f"Discovery {disc_id} found {data['numDevices']} devices")
            success = True
            break

    # If the for loop didn't set the Success variable to True is means that has not finished and taht the timeout is expired
    if not success:
        raise TimeoutError("The discovery didn't complete in time!")

    # If completed then we can create files with the results
    dirpath = os.path.dirname(__file__)
    file_dir = f"{dirpath}/disc_output/{disc_id}"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # Get a list of the discovered devices and their status
    dev_sum = dnac._req(
        f"dna/intent/api/v1/discovery/{disc_id}/network-device")

    # Iterate through the discovered devices

    for dev in dev_sum.json()['response']:
        # if the device were reachable via CLI or SNMP
        if dev['reachabilityStatus'].lower() == "success":
            print(f"{dev['hostname']} success")

            # ...and they are already in the system as managed devices
        if dev['inventoryReachabilityStatus'].lower() == "reachable":
            get_dev = dnac._req(
                f"dna/intent/api/v1/network-device/{dev['id']}")

            # Create a top-level dict with "discovery" and "device" keys
            output = {"discovery": dev, "device": get_dev.json()['response']}
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
