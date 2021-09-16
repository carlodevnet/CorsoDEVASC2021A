import requests
import time

# Create a class DNACRequester to support all the requests to DNA Center Intent API
class DNACRequester:

    def __init__(self, host, username, password, verify=True, old_style=False):

        # Constructor to create a new DNA objcet
        self.host = host
        self.verify = verify

        # Disable Warnings
        if not verify:
            requests.packages.urllib3.disable_warnings()
        # Build commond headers
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Check if it's an old version of DNA and change the URL accordingly
        if old_style:
            auth_url = "api/system/api/v1/auth/token"
        else:
            auth_url = "dna/system/api/v1/auth/token"

        auth_resp = self._req(resource=auth_url, method="post",
                              auth=(username, password))
        # For troubleshooting                      
        # print(auth_resp.text)
        auth_resp.raise_for_status()
        self.headers['X-Auth-Token'] = auth_resp.json()['Token']
        # print(self.headers)

    def _req(self, resource, method="get", auth=None, jsonbody=None, params=None, raise_for_status=True, verify=False):

        # Issue a generic request based on the value received as arguments
        # print(f"https://{self.host}/{resource}")
        resp = requests.request(
            method=method, url=f"https://{self.host}/{resource}", auth=auth, headers=self.headers, json=jsonbody, params=params, verify=verify)
        # print(resp.text)
        if raise_for_status:
            resp.raise_for_status()
        return resp

    def _wait_for_task(self, task_id, wait_time=5, attempts=3):
        # Wait until the task is complete making the API call synchronoux

        for _ in range(attempts):
            time.sleep(wait_time)

            # Query the DNS center providing the task ID
            task_resp = self._req(f"dna/intent/api/v1/task/{task_id}")
            task_data = task_resp.json()['response']
            #print(json.dumps(task_data, indent=2))

            # If an error occured failed immediately.
            if task_data['isError']:
                reason = task_data.get("failureReason", task_data['progress'])
                raise ValueError(f"Asynch task error: {reason}")

            # isError is false, but we might not be done yet
            if "endTime" in task_data:
                return task_resp

        # if isError is false but we are not done keep looping
        total = wait_time * attempts
        raise TimeoutError(f"Task timed out in {total} seconds")
