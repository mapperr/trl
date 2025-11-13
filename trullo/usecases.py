import os
import subprocess
import tempfile
import urllib
from typing import Optional, Tuple, List

import attr

from trullo.normalizer import Normalizer
from trullo.printer import Printer
from trullo.tclient import TClient
from trullo.tconfig import TConfig
from trullo.trl_board import TrlBoard
from trullo.trl_card import TrlCard
from trullo.trl_list import TrlList


@attr.s(auto_attribs=True)
class Usecases:
    tconfig: TConfig
    tclient: TClient
    shortener: Normalizer
    printer: Printer
    selected_board_id: Optional[str] = attr.ib(default=None)
    selected_board_name: Optional[str] = attr.ib(default=None)

    def get_selected_board(self) -> Tuple[Optional[str], Optional[str]]:
        if os.path.exists(self.tconfig.selected_board_filepath):
            with open(self.tconfig.selected_board_filepath, 'r') as fh:
                selected_board_id, selected_board_name = \
                    fh.readline().split(',', 1)
                self.selected_board_id = selected_board_id
                self.selected_board_name = selected_board_name
                return selected_board_id, selected_board_name
        return None, None

    def open_trello_in_browser(self):
        subprocess.Popen(['xdg-open', 'https://trello.com'])

    def open_selected_board_in_browser(self):
        board = self.tclient.get_board(self.selected_board_id)
        board_url = board.raw_data['shortUrl']
        subprocess.Popen(['xdg-open', board_url])

    def print_board_list(self):
        boards = self.tclient.get_boards()
        self.printer.print_boards(boards)
        if os.path.exists(self.tconfig.selected_board_filepath):
            print(f'\ncurrently selected board: {self.selected_board_name}')
        else:
            print(f'\nselect a board with `trl b <board_shortcut>`')

    def select_board(self, board_shortcut: str):
        boards = self.tclient.get_boards()
        matching_boards: List[TrlBoard] = self.shortener.get_matches(
            board_shortcut,
            boards
        )
        if len(matching_boards) > 1:
            matching_names = \
                [board.get_normalized_name() for board in matching_boards]
            print(
                f'shortcut [{board_shortcut}] matches more than one board: '
                f'{matching_names}')
            return
        board = matching_boards[0]

        # file
        with open(self.tconfig.selected_board_filepath, 'w') as fh:
            fh.write(f'{board.id},{board.raw_data["name"]}')

    def print_board_lists(self):
        board = self.tclient.get_board(self.selected_board_id)
        self.printer.print_board_lists(board)

    def print_lists(self, lists_shortcuts: Optional[List[str]]):
        board = self.tclient.get_board(self.selected_board_id)
        if lists_shortcuts is not None and len(lists_shortcuts) > 0:
            Printer.print_board(board, lists_shortcuts)
        else:
            Printer.print_board(board)

    def print_card(self, card_shortcut: str):
        card = self._get_card(card_shortcut)
        self.printer.print_card(card)

    def open_card_in_browser(self, card_shortcut: str):
        card = self._get_card(card_shortcut)
        subprocess.Popen(['xdg-open', card.raw_data['shortUrl']])

    def create_card(self, target_list_shortcut: str):
        board = self.tclient.get_board(self.selected_board_id)
        matching_lists: List[TrlList] = Normalizer.get_matches(
            target_list_shortcut,
            board.lists
        )
        if len(matching_lists) > 1:
            matching_names = \
                [list_.get_normalized_name() for list_ in matching_lists]
            print(
                f'shortcut [{target_list_shortcut}] '
                f'matches more than one list: '
                f'{matching_names}')
            exit(1)

        if len(matching_lists) == 0:
            print(
                f'shortcut [{target_list_shortcut}] '
                f'does not match any list')
            exit(1)

        list_id = matching_lists[0].id

        new_card_name, new_card_desc = self._edit_card()
        response = self.tclient.new_card(list_id, new_card_name, new_card_desc)
        print(response.get("shortUrl"))

    def update_card(self, card_shortcut: str):
        card = self._get_card(card_shortcut)
        card_new_name, card_new_desc = self._edit_card(card)
        self.tclient.edit_card(card.id, card_new_name, card_new_desc)

    def comment_card(self, card_shortcut: str, comment: str):
        card = self._get_card(card_shortcut)
        self.tclient.comment_card(card.id, comment)

    def move_card(self, card_shortcut: str, target_list_shortcut: str):
        board = self.tclient.get_board(self.selected_board_id)
        matching_lists: List[TrlList] = Normalizer.get_matches(
            target_list_shortcut,
            board.lists
        )
        if len(matching_lists) > 1:
            matching_names = \
                [list_.get_normalized_name() for list_ in
                 matching_lists]
            print(
                f'shortcut [{target_list_shortcut}] '
                f'matches more than one list: '
                f'{matching_names}')
            exit(1)

        if len(matching_lists) == 0:
            print(
                f'shortcut [{target_list_shortcut}] '
                f'does not match any list')
            exit(1)

        list_id = matching_lists[0].id

        card = self._get_card(card_shortcut)

        self.tclient.move_card(card.id, list_id)

    def _get_card(self, card_shortcut):
        board = self.tclient.get_board(self.selected_board_id)
        matching_cards: List[TrlCard] = Normalizer.get_matches(
            card_shortcut,
            board.cards
        )
        if len(matching_cards) > 1:
            matching_names = \
                [matching_card.get_normalized_name()
                 for matching_card in matching_cards]
            print(
                f'shortcut [{card_shortcut}] '
                f'matches more than one card: '
                f'{matching_names}')
            exit(1)

        if len(matching_cards) == 0:
            print(
                f'shortcut [{card_shortcut}] '
                f'does not match any cards')
            exit(1)

        selected_card = matching_cards[0]
        card = self.tclient.get_card(selected_card.id)
        return card

    def _edit_card(self, card_to_edit: TrlCard = None) -> (str, str):
        """
        :param card_to_edit:
        :return: a Tuple with the new name and description of the card
        """
        tempfile_suffix = 'newcard.md'
        clean_card_name = 'New Card Title'
        card_description = 'New Card Description'
        if card_to_edit is not None:
            tempfile_suffix = f'{card_to_edit.id}.md'
            clean_card_name = str(card_to_edit.raw_data['name']).replace('\n',
                                                                         '')
            card_description = card_to_edit.raw_data['desc']

        tmpfile_path = f'{tempfile.gettempdir()}/.trl-{tempfile_suffix}'
        with open(tmpfile_path, 'w') as fd:
            fd.writelines(
                f"# The line below is the card title, "
                f"lines after that are the card description\n"
                f"{clean_card_name}\n{card_description}")
        subprocess.Popen([os.environ.get('EDITOR'), tmpfile_path]).wait()
        with open(tmpfile_path, 'r') as fd:
            lines = fd.readlines()
        return urllib.parse.quote(lines[1].replace('\n', ''), safe=''), \
               urllib.parse.quote(str.join('', lines[2:]), safe='')

    def print_board_labels(self):
        board = self.tclient.get_board(self.selected_board_id)
        for label in board.labels:
            print('[{}]   {:10} {}'.format(
                label.id, label.color or "", label.name))

    def print_board_members(self):
        board = self.tclient.get_board(self.selected_board_id)
        for member in board.members:
            print('[{}]   {:10} (@{})'.format(
                member.id, member.fullname, member.username))
