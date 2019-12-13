from typing import Dict

import attr

from trullo.shortener import Shortener


@attr.s(auto_attribs=True)
class TrlCard:
    id: str
    short_link: str
    raw_data: Dict

    def get_normalized_name(self):
        return Shortener.normalize(self.raw_data['name'])
