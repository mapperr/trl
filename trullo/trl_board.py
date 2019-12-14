from typing import Dict, List

import attr

from trullo.shortcuttable import Shortcuttable
from trullo.shortener import Shortener
from trullo.trl_card import TrlCard
from trullo.trl_list import TrlList


@attr.s(auto_attribs=True)
class TrlBoard(Shortcuttable):
    id: str
    short_link: str
    lists: List[TrlList]
    cards: List[TrlCard]
    raw_data: Dict

    def get_normalized_name(self) -> str:
        return Shortener.normalize(
            f"{self.raw_data['name']}{self.raw_data['shortLink']}"
        )
