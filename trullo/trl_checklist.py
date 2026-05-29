from typing import List, Optional

import attr


@attr.s(auto_attribs=True)
class TrlCheckItem:
    id: str
    name: str
    state: str
    due: Optional[str]
    id_member: Optional[str]


@attr.s(auto_attribs=True)
class TrlChecklist:
    id: str
    name: str
    id_card: str
    check_items: List[TrlCheckItem]
