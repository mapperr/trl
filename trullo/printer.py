import pprint
from typing import List

import attr

from trullo.shortener import Shortener
from trullo.trl_board import TrlBoard
from trullo.trl_card import TrlCard
from trullo.trl_list import TrlList


@attr.s(auto_attribs=True)
class Printer:
    @staticmethod
    def print_boards(boards: List[TrlBoard]):
        symbol_count = Shortener.get_min_symbols_to_uniq([board.id for board in boards])
        for board in boards:
            print(f"{board.id[0:symbol_count]} [{board.id}] {board.raw_data['name']}")
            if board.lists is not None:
                Printer.print_lists(board.lists, '\t')

    @staticmethod
    def print_lists(lists: List[TrlList], prefix: str = ''):
        symbol_count = Shortener.get_min_symbols_to_uniq([list_.id for list_ in lists])
        for list_ in lists:
            print(f"{prefix}{list_.id[0:symbol_count]} [{list_.id}] {list_.raw_data['name']}")
            if list_.cards is not None:
                Printer.print_cards(list_.cards, f'{prefix}\t')

    @staticmethod
    def print_cards(cards: List[TrlCard], prefix: str = ''):
        symbol_count = Shortener.get_min_symbols_to_uniq([card.id for card in cards])
        for card in cards:
            print(f"{prefix}{card.id[0:symbol_count]} [{card.id}] {card.raw_data['name']}")

    @staticmethod
    def print_card(card: TrlCard):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(card.raw_data)
