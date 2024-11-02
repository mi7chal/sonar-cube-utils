import requests
from functions import *

# config
dotenv = load_dotenv()

# default php rules
url = f"{dotenv.get('API_URL')}/rules/search?languages=php&qprofile=f2fb0cc0-9ffd-4c8d-a66e-42988643234a&activation=true"

rules = load_search_request(url, dotenv.get("TOKEN"), "rules")

export(rules, "php_default_rules.json")

# all php rules
url = f"{dotenv.get('API_URL')}/rules/search?languages=php"

rules = load_search_request(url, dotenv.get("TOKEN"), "rules")

export(rules, "php_rules.json")