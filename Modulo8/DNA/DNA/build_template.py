import os
import json
from DNAC_Requestor import DNACRequester


def main():

    dnac = DNACRequester(host="10.10.20.85", username="admin",
                         password="Cisco1234!", verify=False)

    proj_body = {
        "name": "FF_Project-FINAL-DAVVEROFINAL",
        "description": "FiveFold Lab Project",
    }

    proj_resp = dnac._req(
        f"dna/intent/api/v1/template-programmer/project", method="post", jsonbody=proj_body)

    proj_task = dnac._wait_for_task(proj_resp.json()['response']['taskId'])
    proj_id = proj_task.json()['response']['data']

    dirpath = os.path.dirname(__file__)
    for template in os.listdir(f"{dirpath}/templates"):
        with open(f"{dirpath}/templates/{template}", "r") as handle:
            temp_data = json.load(handle)

        print(f"Creating template from {template}")
        # print(temp_data)
        creation_resp = dnac._req(
            f"dna/intent/api/v1/template-programmer/project/{proj_id}/template", method="post", jsonbody=temp_data['body'])

        #print(json.dumps(creation_resp.json()), indent=2)

        temp_task = dnac._wait_for_task(
            creation_resp.json()['response']['taskId'])
        temp_id = temp_task.json()['response']['data']

        prev_body = {"params": temp_data['params'], "templateId": temp_id}

        prev_data = dnac._req(
            f"dna/intent/api/v1/template-programmer/template/preview", method="put", jsonbody=prev_body).json()

        print(f"Checking the template...")
        if prev_data['validationErrors']:
            print(f"Errors:")
            for error in prev_data['validationErrors']:
                print(f"{error['type']} : {error['message']}")
        else:
            print(f"Snippet rendered!")
            print(f"{prev_data['cliPreview']}")
            version_and_deploy(dnac, temp_data, temp_id)


def version_and_deploy(dnac, temp_data, temp_id, ip_addr="10.10.20.81"):
    ver_body = {"comments": "First commit via API", "templateId": temp_id}
    ver_resp = dnac._req(
        "dna/intent/api/v1/template-programmer/template/version", method="post", jsonbody=ver_body)

    ver_task = dnac._wait_for_task(ver_resp.json()['response']['taskId'])
    print(f"Version status: {ver_task.json()['response']['progress']}")

    deploy_body = {
        "forcePushTemplate": "false",
        "targetInfo": [
            {
                "id": ip_addr,
                "params": temp_data['params'],
                "type": "MANAGED_DEVICE_IP"
            }
        ],
        "templateId": temp_id
    }

    deploy_resp = ver_resp = dnac._req(
        "dna/intent/api/v1/template-programmer/template/deploy", method="post", jsonbody=deploy_body)
    print(f"Deployement Id: {deploy_resp.json()['deploymentId']}")


if __name__ == "__main__":
    main()
