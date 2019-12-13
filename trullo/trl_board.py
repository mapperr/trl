from typing import Dict, List

import attr

from trullo.shortener import Shortener
from trullo.trl_list import TrlList
from trullo.trl_card import TrlCard


@attr.s(auto_attribs=True)
class TrlBoard:
    id: str
    short_link: str
    lists: List[TrlList]
    cards: List[TrlCard]
    raw_data: Dict

    def get_normalized_name(self) -> str:
        return Shortener.normalize(self.raw_data['name'])
