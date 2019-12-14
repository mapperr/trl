from typing import Dict

import attr

from trullo.shortcuttable import Shortcuttable
from trullo.shortener import Shortener


@attr.s(auto_attribs=True)
class TrlList(Shortcuttable):
    id: str
    raw_data: Dict

    def get_normalized_name(self) -> str:
        return Shortener.normalize(self.raw_data['name'])
