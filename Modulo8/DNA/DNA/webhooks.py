from DNAC_Requestor import DNACRequester
import time


def main():

    dnac = DNACRequester(host="10.10.20.85", username="admin",
                         password="Cisco1234!", verify=False)

    events = dnac._req(f"dna/intent/api/v1/events",
                       params={"tags": "ASSURANCE"}).json()

    #import json
    # print(json.dumps(events,
    #                 indent=2))

    # events_ids = [event['eventId'] for event in events.json()]

    eventsids = []
    for event in events:
        event_id_name = event['eventId']
        eventsids.append(event_id_name)

    body = [
        {
            "name": "FiveFold_Assurance",
            "description": "Description",
            "subscriptionEndpoints": [
                {
                    "subscriptionDetails": {
                        "name": "webhook.site",
                        "url": "https://webhook.site/8df116fa-24b0-4eb8-99fd-cdd335bb53fe",
                        "description": "WebHook.site Webhook",
                        "method": "POST",
                        "connectorType": "REST"
                    }
                }
            ],
            "filter": {"eventIds": eventsids},
        }
    ]

    resp = dnac._req("dna/intent/api/v1/event/subscription",
                     method="post", jsonbody=body)

    time.sleep(10)

    add_status = dnac._req(resp.json()['statusUri'][1:]).json()

    if add_status['errorMessage']:
        raise ValueError(f"{add_status['errorMessage']}")

    print(f"{add_status['statusMessage']} / {add_status['apiStatus']}")

    subs_resp = dnac._req(f"dna/intent/api/v1/event/subscription")

    my_sub = subs_resp.json()[-1]
    print(
        f"Confirmed that {my_sub['name']} using ID {my_sub['subscriptionId']}")


if __name__ == "__main__":
    main()
