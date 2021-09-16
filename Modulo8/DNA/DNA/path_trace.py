import os
import json
from DNAC_Requestor import DNACRequester


def main():

    dnac = DNACRequester(host="10.10.20.85", username="admin",
                         password="Cisco1234!", verify=False)

    body = {
        "sourceIP": "10.10.20.81",
        "destIP": "10.10.20.82",
        "inclusions": [
            "INTERFACE-STATS", "DEVICE-STATS", "QOS-STATS"
        ],
        "controlPath": False,
        "periodicRefresh": False,
    }

    path = dnac._req("dna/intent/api/v1/flow-analysis",
                     method="post", jsonbody=body)

    path_data = path.json()['response']
    task_status = dnac._wait_for_task(path_data['taskId'])

    if task_status.json()['response']['progress'] != path_data['flowAnalysisId']:
        raise ValueError(
            "Unexpected error; Task progress doesn't match flow id")

    flow_resp = dnac._req(
        f"dna/intent/api/v1/flow-analysis/{path_data['flowAnalysisId']}")

    print(json.dumps(flow_resp.json(), indent=2))

    flow_data = flow_resp.json()['response']

    print(f"Path trace {flow_data['request']['sourceIP']} --> "
          f"{flow_data['request']['destIP']}")

    for i, hop in enumerate(flow_data['networkElementsInfo']):
        print(f"Hop {i+1}: {hop['name']}")
        # if i == 0:
        #     print(
        #         f"Egress Interface: {hop['egressInterface']['physicalInterface']['name']}")
        # elif i > 0 and i < enumerate(flow_data['networkElementsInfo']):
        #     print(
        #         f"Egress Interface: {hop['egressInterface']['physicalInterface']['name']}")
        #     print(
        #         f"Ingress Interface: {hop['ingressInterface']['physicalInterface']['name']}")
        # elif i == enumerate(flow_data['networkElementsInfo']):
        #     print(
        #         f"Ingress Interface: {hop['ingressInterface']['physicalInterface']['name']}")


if __name__ == "__main__":
    main()
