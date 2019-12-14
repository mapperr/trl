from typing import List
from typing import Set

import attr

from trullo.shortcuttable import Shortcuttable


@attr.s(auto_attribs=True)
class Shortener:
    @staticmethod
    def normalize(string: str) -> str:
        result = ''
        for char in string:
            if char.lower() not in 'qwertyuiopasdfghjklzxcvbnm1234567890':
                continue
            result += char.lower()
        return result

    @staticmethod
    def get_min_symbols_to_uniq(strings: List[str]) -> int:
        symbol_counter = 1
        longest_item_length = Shortener.get_longest_item_length(strings)
        string_list = [
            string_item[0:symbol_counter].lower()
            for string_item in strings
        ]
        while symbol_counter < longest_item_length \
                and Shortener.are_there_duplicates(string_list):
            symbol_counter += 1
            string_list = [
                string_item[0:symbol_counter].lower()
                for string_item in strings
            ]
        return symbol_counter

    @staticmethod
    def are_there_duplicates(list_: List[str]):
        set_: Set[str] = set()
        for elem in list_:
            if elem in set_:
                return True
            else:
                set_.add(elem)
        return False

    @staticmethod
    def get_longest_item_length(list_: List[str]) -> int:
        longest_length = 0
        for string in list_:
            length = len(string)
            if length > longest_length:
                longest_length = length
        return longest_length

    @staticmethod
    def get_matches(shortcut: str,
                    shortcuttables: List[Shortcuttable]) \
            -> List[any]:
        return [shortcuttable for shortcuttable in shortcuttables
                if shortcut in shortcuttable.get_normalized_name()]
