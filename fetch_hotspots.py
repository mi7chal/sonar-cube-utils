import requests
from functions import *

# config
dotenv = load_dotenv()
api_url = dotenv.get("API_URL")
auth_token = dotenv.get("TOKEN")
project_key = dotenv.get("PROJECT_KEY")

headers = {"Authorization": f"Bearer {auth_token}"}

hasMore = True
page = 1
high_vulnerability = []
while hasMore:
    response = requests.get(f"{api_url}/hotspots/search?project={project_key}&ps=500&p={page}",
                            headers=headers)

    hotspots = response.json()["hotspots"]

    if len(hotspots) < 500:
        hasMore = False
        print(len(hotspots))


    for hotspot in hotspots:

        if hotspot["vulnerabilityProbability"] == "HIGH":
            high_vulnerability.append(hotspot)
            print(f"Appending {hotspot['key']}")

    page += 1


export(high_vulnerability, "security_hotspots.json")