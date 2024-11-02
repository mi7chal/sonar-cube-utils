import json
import os
from configparser import ConfigParser

import requests
from dotenv import dotenv_values


def find_element_key(element):
    if type(element) != dict:
        raise TypeError("Issue must be a dictionary")

    if "key" not in element:
        raise TypeError("Issue must have a 'key' field")

    return element["key"]

def export(to_export, file_name):
    config = ConfigParser()

    config.read("config.ini")

    if not file_name.endswith(".json"):
        file_name += ".json"

    print(config.defaults())

    export_directory = config.get('', 'ExportDir', fallback="exports")

    if len(export_directory) > 0 and not export_directory.endswith("/"):
        export_directory += "/"

    absolute_path = export_directory + file_name

    if not os.path.exists(export_directory):
        os.makedirs(export_directory)

    f = open(absolute_path, "w")
    f.write(json.dumps(to_export))
    f.close()


def load_dotenv():
    return dotenv_values()

def load_search_request(full_url: str, api_key: str, response_key: str):
    # pagination in sonar starts from 1
    page = 1
    full_list = []

    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"Fetching list from {full_url}")

    if "?" in full_url:
        full_url += "&"
    else:
        full_url += "?"

    full_url += "ps=500"

    while True:
        response = requests.get(full_url + f"&p{page}",headers=headers)

        objects = response.json()[response_key]

        for obj in objects:
            full_list.append(obj)
            print(f"Appending {obj['key']}")

        if len(objects) < 500:
            print(f"Loaded {len(objects)} from url {full_url}.")
            break

        page += 1

    return full_list

