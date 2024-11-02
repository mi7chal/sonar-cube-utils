import requests
from functions import *

# config
sonar_api_url = "http://localhost:9000/api"
auth_token = "squ_10947294ae890425f2a46dce469099f28ea08fd8" # must be an admin key
project_key = "Moodle"

headers = {"Authorization": f"Bearer {auth_token}"}


max_issues = 0
total_issues = 1
# looping over all existing open issues
while total_issues > 0:
    # fetching issues
    response = requests.get(f"{sonar_api_url}/issues/search?componentKeys={project_key}&ps=500&issueStatuses=OPEN", headers=headers)
    json = response.json()
    issues = json["issues"]
    total_issues = json["total"]

    current_part_length = len(issues)

    # saving issues total length
    if max_issues == 0:
        max_issues = total_issues

    print(f"Looping over {current_part_length} issues, left: {total_issues}")

    # updating issues
    issues_keys = map(find_element_key, issues)
    bulk_change_response = requests.post(f"{sonar_api_url}/issues/bulk_change?issues={','.join(issues_keys)}&add_tags=moodle-scope&do_transition=accept", headers=headers)

    if not bulk_change_response.ok:
        raise Exception(f"Bulk change request failed with status code {bulk_change_response.status_code}.")

    print(f"Successfully updated {current_part_length} issues.")


print(f"\nFinished modifying {max_issues} issues. Now handling security hotspots.\n")

max_hotspots = 0
total_hotspots = 1
# looping over all existing open security hotspots
while total_hotspots > 0:
    # fetching issues
    response = requests.get(f"{sonar_api_url}/hotspots/search?project={project_key}&ps=500&status=TO_REVIEW", headers=headers)
    json = response.json()

    hotspots = json["hotspots"]
    total_hotspots = json["paging"]["total"]

    current_part_length = len(hotspots)

    # saving issues total length
    if max_hotspots == 0:
        max_hotspots = total_hotspots

    print(f"Looping over {current_part_length} hotspots, left: {total_hotspots}")

    # updating hotspots
    for hotspot in hotspots:
        response_hotspot_change = requests.post(f"{sonar_api_url}/hotspots/change_status?hotspot={hotspot['key']}&resolution=SAFE&status=REVIEWED", headers=headers)

        if not response_hotspot_change.ok:
            raise Exception(f"Hotspot change with key {hotspot['key']} failed with status code {response_hotspot_change.status_code}.")

        print(f"Updated hotspot {hotspot['key']}")


    print(f"Successfully updated {current_part_length} hotspots.")

print(f"\nFinished modifying {max_issues} issues and {max_hotspots} security hotspots. Exiting..")

