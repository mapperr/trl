from typing import Dict, Optional

import attr

from trullo.normalizer import Normalizer
from trullo.shortcuttable import Shortcuttable


@attr.s(auto_attribs=True)
class TrlLabel(Shortcuttable):
    id: str
    name: str
    raw_data: Dict
    color: Optional[str] = attr.ib(default=None)

    def get_normalized_name(self) -> str:
        return Normalizer.normalize(
            f"{self.raw_data['name']}"
            f"{self.color if self.color is not None else ''}"
            f"{self.id}"
        )
