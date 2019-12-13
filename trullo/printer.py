from typing import List

import attr

from trullo.shortener import Shortener
from trullo.trl_board import TrlBoard
from trullo.trl_card import TrlCard


@attr.s(auto_attribs=True)
class Printer:
    @staticmethod
    def print_boards(boards: List[TrlBoard]):
        symbol_count = Shortener. \
            get_min_symbols_to_uniq([board.get_normalized_name()
                                     for board in boards])
        print(f'symbol count is {symbol_count}')
        for board in boards:
            print(
                f"[{board.get_normalized_name()[0:symbol_count].lower()}] "
                f"{board.raw_data['name']}")

    @staticmethod
    def print_board(board: TrlBoard, list_shortcut: str = None):
        cards_names = [card.get_normalized_name() for card in board.cards]
        board_lists_names = \
            [list_.get_normalized_name() for list_ in board.lists]

        symbol_count_cards = Shortener.get_min_symbols_to_uniq(cards_names)
        symbol_count_lists = \
            Shortener.get_min_symbols_to_uniq(board_lists_names)

        print(f"{board.raw_data['shortUrl']}")
        print('------------------------------')
        print(f"{board.raw_data['name']}")
        print()
        if board.lists is not None:
            for list_ in board.lists:
                if list_shortcut is not None \
                        and not \
                        list_.get_normalized_name().startswith(list_shortcut):
                    continue
                shortcut = \
                    list_.get_normalized_name()[0:symbol_count_lists].lower()
                print(f"[{shortcut}] {list_.raw_data['name']}")
                for card in board.cards:
                    if card.raw_data['idList'] == list_.id:
                        card_shortcut = card.get_normalized_name()[
                                        0:symbol_count_cards].lower()
                        print(f"\t[{card_shortcut}] "
                              f"{card.raw_data['name']}")
        print()

    @staticmethod
    def print_board_lists(board: TrlBoard):
        symbol_count_lists = Shortener.get_min_symbols_to_uniq(
            [list_.get_normalized_name() for list_ in board.lists])
        print(f"{board.raw_data['shortUrl']}")
        print('------------------------------')
        print(f"{board.raw_data['name']}")
        print()
        if board.lists is not None:
            for list_ in board.lists:
                list_shortcut = \
                    list_.get_normalized_name()[0:symbol_count_lists].lower()
                print(f"[{list_shortcut}] {list_.raw_data['name']}")
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
        for label in d['labels']:
            label_name = label["name"] \
                if label["name"] is not None and label["name"] != "" \
                else label["color"]
            print(f'({label_name})  ', end='')
        print()
        print(formatted_desc)
        print()
