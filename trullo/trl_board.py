from typing import Dict, List

import attr

from trullo.normalizer import Normalizer
from trullo.shortcuttable import Shortcuttable
from trullo.trl_card import TrlCard
from trullo.trl_label import TrlLabel
from trullo.trl_list import TrlList
from trullo.trl_member import TrlMember


@attr.s(auto_attribs=True)
class TrlBoard(Shortcuttable):
    id: str
    short_link: str
    lists: List[TrlList]
    cards: List[TrlCard]
    labels: List[TrlLabel]
    members: List[TrlMember]
    raw_data: Dict

    def get_normalized_name(self) -> str:
        return Normalizer.normalize(
            f"{self.raw_data['name']}{self.raw_data['shortLink']}"
        )

    def find_member(self, id: str) -> TrlMember | None:
        for member in self.members:
            if member.id == id:
                return member
