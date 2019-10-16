import os
from typing import Dict

import attr
import requests


@attr.s(auto_attribs=True)
class TClient:
    trello_token: str = attr.ib(default=os.environ['TRELLO_TOKEN'] if 'TRELLO_TOKEN' in os.environ else '')
    trello_api_key: str = attr.ib(default=os.environ['TRELLO_API_KEY'] if 'TRELLO_API_KEY' in os.environ else '')
    base_url: str = attr.ib(default='https://api.trello.com/1')

    def build_auth_params(self) -> Dict[str, str]:
        return {'key': self.trello_api_key, 'token': self.trello_token}

    def get(self, path: str) -> str:
        return requests.get(self.base_url + path, self.build_auth_params()).json()
