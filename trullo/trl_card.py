from typing import Dict

import attr

from trullo.shortcuttable import Shortcuttable
from trullo.normalizer import Normalizer


@attr.s(auto_attribs=True)
class TrlCard(Shortcuttable):
    id: str
    short_link: str
    raw_data: Dict

    def get_normalized_name(self):
        return Normalizer.normalize(
            f"{self.raw_data['name']}{self.raw_data['shortLink']}"
        )
