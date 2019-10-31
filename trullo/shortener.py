from typing import List

import attr


@attr.s(auto_attribs=True)
class Shortener:
    @staticmethod
    def get_min_symbols_to_uniq(strings: List[str], end: bool = False) -> int:
        symbol_counter = 1
        longest_item_length = Shortener.get_longest_item_length(strings)
        if end:
            while symbol_counter < longest_item_length \
                    and Shortener.are_there_duplicates([el[len(el)-symbol_counter:len(el)].lower() for el in strings]):
                symbol_counter += 1
        else:
            while symbol_counter < longest_item_length \
                    and Shortener.are_there_duplicates([el[0:symbol_counter].lower() for el in strings]):
                symbol_counter += 1
        return symbol_counter

    @staticmethod
    def are_there_duplicates(list_):
        set_ = set()
        for elem in list_:
            if elem in set_:
                return True
            else:
                set_.add(elem)
        return False

    @staticmethod
    def get_longest_item_length(list_: List[str]) -> int:
        longest = 0
        for string in list_:
            length = len(string)
            if length > longest:
                longest = length
        return longest
