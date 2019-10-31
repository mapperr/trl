from typing import List

import attr

from trullo.shortener import Shortener
from trullo.trl_board import TrlBoard
from trullo.trl_card import TrlCard


@attr.s(auto_attribs=True)
class Printer:
    @staticmethod
    def print_boards(boards: List[TrlBoard]):
        symbol_count = Shortener.get_min_symbols_to_uniq([board.shortcut.lower() for board in boards])
        for board in boards:
            print(f"[{board.shortcut[0:symbol_count].lower()}] {board.raw_data['name']}")

    @staticmethod
    def print_board(board: TrlBoard, list_shortcut: str = None):
        symbol_count_cards = Shortener.get_min_symbols_to_uniq([card.shortcut for card in board.cards])
        symbol_count_lists = Shortener.get_min_symbols_to_uniq([list_.id for list_ in board.lists], True)
        print(f"{board.raw_data['shortUrl']}")
        print('------------------------------')
        print(f"{board.raw_data['name']}")
        print()
        if board.lists is not None:
            for list_ in board.lists:
                if list_shortcut is not None and not list_.id.lower().endswith(list_shortcut):
                    continue
                print(
                    f"[{list_.id[len(list_.id) - symbol_count_lists:len(list_.id)].lower()}] {list_.raw_data['name']}")
                for card in board.cards:
                    if card.raw_data['idList'] == list_.id:
                        print(f"\t[{card.shortcut[0:symbol_count_cards].lower()}] {card.raw_data['name']}")
        print()

    @staticmethod
    def print_card(card: TrlCard):
        d = card.raw_data
        formatted_desc = '\t' + str(d['desc']).replace('\n', '\n\t')

        print(f'{d["shortUrl"]}')
        print('-------------------------------------')
        print(f'{d["name"]}')
        if len(d['labels']) > 0:
            print()
        for l in d['labels']:
            print(f'({l["name"] if l["name"] is not None and l["name"] != "" else l["color"]})  ', end='')
        print()
        print(formatted_desc)
        print()
