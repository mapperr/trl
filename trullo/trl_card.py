from typing import Dict

import attr


@attr.s(auto_attribs=True)
class TrlCard:
    id: str
    raw_data: Dict
