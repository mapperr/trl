from typing import Dict, List

import attr

from trullo.normalizer import Normalizer
from trullo.shortcuttable import Shortcuttable
from trullo.trl_card import TrlCard
from trullo.trl_checklist import TrlChecklist
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
    checklists: List[TrlChecklist]
    raw_data: Dict

    def get_normalized_name(self) -> str:
        return Normalizer.normalize(
            f"{self.raw_data['name']}{self.raw_data['shortLink']}"
        )

    def find_member(self, id: str) -> TrlMember | None:
        for member in self.members:
            if member.id == id:
                return member

    def find_list(self, id: str) -> TrlList | None:
        for list_ in self.lists:
            if list_.id == id:
                return list_

    def find_checklists_for_card(self, card_id: str) -> List[TrlChecklist]:
        return [cl for cl in self.checklists if cl.id_card == card_id]
