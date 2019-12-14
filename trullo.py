"""Trullo

usage:
    trl b [<board_shortcut>]
    trl l [<list_shortcuts>...]
    trl ll
    trl c <card_shortcut> [o | m <list_shortcut> | e | n <list_shortcut>]
    trl c n <list_shortcut>
    trl g <api_path>
    trl -h

    -h --help  this help message


commands:
    b [<board_shortcut>]
        shows the boards you can access
        with board_shortcut you can select the board you want to work with

    l [<list_shortcuts>...]
        shows lists and cards in the board you have currently selected
        with list_shortcuts you can show only selected lists and their cards

    ll
        shows only the board's lists

    c <card_shortcut> [o | m <list_shortcut> | e]
        shows the card infos
        with o it opens the card shortLink with your default browser
        with m and a target list you can move the card to that list
        with e you can edit the card title and description in your $EDITOR

    c n <list_shortcut>
        create a new card in the list specified by list_shortcut

    g <api_path>
        make a direct api call adding auth params automatically (for debugging/hacking purpose)

env:
    you have to export this 2 variables to authenticate with trello:

    TRELLO_API_TOKEN - your trello api key
    TRELLO_TOKEN - a generated token

    you can obtain those values here: https://trello.com/app-key

"""
import logging
import os
import pprint
import subprocess
import tempfile
import urllib
from typing import List

from docopt import docopt

from trullo.printer import Printer
from trullo.shortener import Shortener
from trullo.tclient import TClient
from trullo.trl_board import TrlBoard
from trullo.trl_card import TrlCard
# logging.basicConfig(level=logging.DEBUG)
from trullo.trl_list import TrlList

logging.basicConfig(level=logging.INFO)
logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def edit_card(card_to_edit: TrlCard = None) -> (str, str):
    """
    :param card_to_edit:
    :return: a Tuple with the new name and description of the card
    """
    tempfile_suffix = 'newcard.md'
    clean_card_name = 'New Card Title'
    card_description = 'New Card Description'
    if card_to_edit is not None:
        tempfile_suffix = f'{card.id}.md'
        clean_card_name = str(card_to_edit.raw_data['name']).replace('\n', '')
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


if __name__ == '__main__':
    args = docopt(__doc__, version='Trullo beta')

    tclient = TClient()

    tmpdir = tempfile.gettempdir()
    selected_board_filepath = f'{tmpdir}/.trl-selected-board'
    if os.path.exists(selected_board_filepath):
        with open(selected_board_filepath, 'r') as fh:
            selected_board_id, selected_board_name = fh.readline().split(
                ' ', 1)

    if args['g']:
        api_path = args['<api_path>']
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(tclient.get(api_path))

    if args['b']:
        boards = tclient.get_boards()
        if args['<board_shortcut>']:
            board_shortcut = args['<board_shortcut>']
            matching_boards: List[TrlBoard] = Shortener.get_matches(
                board_shortcut,
                boards
            )
            if len(matching_boards) > 1:
                matching_names = \
                    [board.get_normalized_name() for board in matching_boards]
                print(
                    f'shortcut [{board_shortcut}] matches more than one board: '
                    f'{matching_names}')
                exit(1)
            board = matching_boards[0]
            print(f'selected board {board.raw_data["name"]}')
            with open(selected_board_filepath, 'w') as fh:
                fh.write(f'{board.id} {board.raw_data["name"]}')
        else:
            Printer.print_boards(boards)
            if os.path.exists(selected_board_filepath):
                print(f'\ncurrently selected board: {selected_board_name}')
            else:
                print(f'\nselect a board with `trl b <board_shortcut>`')

    # stuff that works only if a board is selected
    if not args['b'] and not os.path.exists(selected_board_filepath):
        print(f'first select a board with `trl b`')
        exit(1)

    if args['ll']:
        board = tclient.get_board(selected_board_id)
        Printer.print_board_lists(board)

    if args['l']:
        board = tclient.get_board(selected_board_id)
        list_shortcuts = args['<list_shortcuts>']
        if list_shortcuts is not None and len(list_shortcuts) > 0:
            Printer.print_board(board, list_shortcuts)
        else:
            Printer.print_board(board)

    if args['c']:
        board = tclient.get_board(selected_board_id)
        new_command = args['n']
        if new_command:
            target_list_shortcut = args['<list_shortcut>']
            matching_lists: List[TrlList] = Shortener.get_matches(
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
            list_id = matching_lists[0].id

            new_card_name, new_card_desc = edit_card()
            tclient.new_card(list_id, new_card_name, new_card_desc)
        else:
            card_shortcut = args['<card_shortcut>']
            matching_cards: List[TrlCard] = Shortener.get_matches(
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

            selected_card = matching_cards[0]
            card = tclient.get_card(selected_card.id)

            open_command = args['o']
            move_command = args['m']
            edit_command = args['e']
            if open_command:
                subprocess.Popen(['xdg-open', card.raw_data['shortUrl']])
            elif move_command:
                target_list_shortcut = args['<list_shortcut>']
                matching_lists: List[TrlList] = Shortener.get_matches(
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
                list_id = matching_lists[0].id

                tclient.move_card(card.id, list_id)
            elif edit_command:
                card_new_name, card_new_desc = edit_card(card)
                logger.debug(card_new_desc)
                tclient.edit_card(card.id, card_new_name, card_new_desc)
            else:
                Printer.print_card(card)
