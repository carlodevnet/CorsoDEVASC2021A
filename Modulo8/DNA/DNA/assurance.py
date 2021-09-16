import os
import json
from DNAC_Requestor import DNACRequester
import time


def main():

    dnac = DNACRequester(host="10.10.20.85", username="admin",
                         password="Cisco1234!", verify=False)

    dirpath = os.path.dirname(__file__)
    health_dir = "health_output"
    if not os.path.exists(f"{dirpath}/{health_dir}"):
        os.makedirs(f"{dirpath}/{health_dir}")

    current_epoch = int(time.time() * 1000)
    params = {"timestamp": current_epoch}

    for health in ["network", "site", "client"]:
        health_resp = dnac._req(
            f"dna/intent/api/v1/{health}-health", params=params)

        with open(f"{dirpath}/{health_dir}/get_{health}.json", "w") as handle:
            json.dump(health_resp.json(), handle, indent=2)
        print(f"Wrote {health} health to disk")


if __name__ == "__main__":
    main()
