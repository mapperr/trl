from typing import List, Optional

import attr

from trullo.normalizer import Normalizer
from trullo.trl_board import TrlBoard
from trullo.trl_card import TrlCard


@attr.s(auto_attribs=True)
class Printer:
    @staticmethod
    def print_boards(boards: List[TrlBoard]):
        for board in boards:
            print(f"[{board.raw_data['shortLink']}] "
                  f"{board.raw_data['name']}")

    @staticmethod
    def print_board(board: TrlBoard,
                    list_shortcuts: Optional[List[str]] = None):
        print(f"{board.raw_data['shortUrl']}")
        print('------------------------------')
        print(f"{board.raw_data['name']}")
        print()
        if board.lists is not None:
            matching_lists = board.lists
            if list_shortcuts is not None and len(list_shortcuts) > 0:
                matching_lists = [
                    list_ for list_ in board.lists
                    if Printer._there_is_a_match(
                        list_.get_normalized_name(),
                        list_shortcuts)
                ]
            for list_ in matching_lists:
                print(f"\n{list_.raw_data['name']}\n"
                      f"[{list_.raw_data['id'].lower()}]")
                for card in board.cards:
                    if card.raw_data['idList'] == list_.id:
                        card_output = \
                            f"\n\t{card.raw_data['name']}" \
                            f"\n\t[{card.raw_data['shortLink']}] "
                        for raw_label in card.raw_data['labels']:
                            card_output += f'({raw_label["name"]}) '
                        print(card_output)
        print()

    @staticmethod
    def print_board_lists(board: TrlBoard):
        print(f"{board.raw_data['shortUrl']}")
        print('------------------------------')
        print(f"{board.raw_data['name']}")
        print()
        if board.lists is not None:
            for list_ in board.lists:
                print(f"[{list_.raw_data['id'].lower()}] "
                      f"{list_.raw_data['name']}")
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

    @staticmethod
    def _there_is_a_match(normalized_name: str, shortcuts: List[str]) -> bool:
        return len([
            shortcut for shortcut in shortcuts
            if Normalizer.is_a_match(shortcut, normalized_name)
        ]) > 0
