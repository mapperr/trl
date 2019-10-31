from typing import List, Dict

import attr

from trullo.trl_card import TrlCard


@attr.s(auto_attribs=True)
class TrlList:
    id: str
    raw_data: Dict
