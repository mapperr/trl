from typing import Dict, List

import attr

from trullo.trl_list import TrlList


@attr.s(auto_attribs=True)
class TrlBoard:
    id: str
    lists: List[TrlList]
    raw_data: Dict
