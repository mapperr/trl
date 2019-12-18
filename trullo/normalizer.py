from typing import List

import attr

from trullo.shortcuttable import Shortcuttable


@attr.s(auto_attribs=True)
class Normalizer:
    @staticmethod
    def normalize(string: str) -> str:
        result = ''
        for char in string:
            if char.lower() not in 'qwertyuiopasdfghjklzxcvbnm1234567890':
                continue
            result += char.lower()
        return result

    @staticmethod
    def get_matches(
            shortcut: str,
            shortcuttables: List[Shortcuttable]) -> List[any]:
        return [
            shortcuttable for shortcuttable in shortcuttables
            if Normalizer.is_a_match(
                shortcut,
                shortcuttable.get_normalized_name())]

    @staticmethod
    def is_a_match(shortcut: str, normalized_name: str) -> bool:
        return shortcut in normalized_name
