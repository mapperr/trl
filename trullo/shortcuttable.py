from abc import abstractmethod

import attr


@attr.s(auto_attribs=True)
class Shortcuttable:
    @abstractmethod
    def get_normalized_name(self) -> str:
        pass
