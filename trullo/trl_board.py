from typing import Dict, List

import attr

from trullo.trl_list import TrlList
from trullo.trl_card import TrlCard


@attr.s(auto_attribs=True)
class TrlBoard:
    id: str
    shortcut: str
    lists: List[TrlList]
    cards: List[TrlCard]
    raw_data: Dict
