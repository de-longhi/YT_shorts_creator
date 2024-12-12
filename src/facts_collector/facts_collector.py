import requests
import random

DEBUG_FACTS = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Vestibulum eget ante volutpat, aliquet purus a, iaculis nibh.",
    "Duis cursus justo ac lectus aliquet posuere.",
    "Praesent ut urna sodales, pellentesque turpis eget, tempor sem.",
    "Nunc rhoncus nibh non magna vehicula, eget rutrum dui faucibus.",
]


class scientist:
    def __init__(self, api_url, api_key, header_keyname="X-Api-Key", debug=False):
        self.api_url = api_url
        self.api_key = api_key
        self.header_key = header_keyname
        self.debug = debug

    def fetch(self):
        if self.debug:
            num = random.randint(0, 4)
            return [DEBUG_FACTS[num]]
        try:
            response = requests.get(
                self.api_url, headers={self.header_key: f"{self.api_key}"}
            )

            response.raise_for_status()
            facts = response.json()
            return [fact["fact"] for fact in facts]

        except requests.exceptions.RequestException as e:
            print(f"Error fetching facts: {e}")
            return None
