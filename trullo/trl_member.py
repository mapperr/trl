from typing import Dict, Optional

import attr

from trullo.normalizer import Normalizer
from trullo.shortcuttable import Shortcuttable


@attr.s(auto_attribs=True)
class TrlMember(Shortcuttable):
    id: str
    fullname: str
    username: str
    raw_data: Dict

    def get_normalized_name(self) -> str:
        return Normalizer.normalize(
            f"{self.fullname}"
            f"{self.username}"
            f"{self.id}"
        )
