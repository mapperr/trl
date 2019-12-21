"""Trullo

usage:
    trl o
    trl b [<board_shortcut>]
    trl l [<list_shortcuts>...]
    trl ll
    trl lb
    trl c <card_shortcut> [o | m <list_shortcut> | e | n <list_shortcut>]
    trl c n <list_shortcut>
    trl g <api_path>
    trl -h

    -h --help  this help message


commands:
    o
        open trello in your browser

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


trello development board: https://trello.com/b/fuK3ff2z

"""
import logging
import pprint
import tempfile

from docopt import docopt

from trullo.printer import Printer
from trullo.normalizer import Normalizer
from trullo.tclient import TClient
from trullo.tconfig import TConfig
from trullo.usecases import Usecases

logging.basicConfig(level=logging.INFO)
logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    args = docopt(__doc__, version='Trullo beta')

    tclient = TClient()

    tmpdir = tempfile.gettempdir()
    selected_board_filepath = f'{tmpdir}/.trl-selected-board'

    usecases = Usecases(TConfig(selected_board_filepath),
                        TClient(),
                        Normalizer(),
                        Printer())

    selected_board_id, selected_board_name = usecases.get_selected_board()

    if args['c']:
        new_command = args['n']
        if new_command:
            target_list_shortcut = args['<list_shortcut>']
            usecases.create_card(target_list_shortcut)
        else:
            card_shortcut = args['<card_shortcut>']
            open_command = args['o']
            move_command = args['m']
            edit_command = args['e']
            if open_command:
                usecases.open_card_in_browser(card_shortcut)
            elif move_command:
                target_list_shortcut = args['<list_shortcut>']
                usecases.move_card(card_shortcut, target_list_shortcut)
            elif edit_command:
                usecases.update_card(card_shortcut)
            else:
                usecases.print_card(card_shortcut)

    elif args['o']:
        usecases.open_trello_in_browser()

    elif args['b']:
        if args['<board_shortcut>']:
            board_shortcut = args['<board_shortcut>']
            usecases.select_board(board_shortcut)
        else:
            usecases.print_board_list()

    # below are stuffs that works only if a board is selected
    elif not args['b'] and selected_board_name is None:
        print(f'first select a board with `trl b`')
        exit(1)

    elif args['ll']:
        usecases.print_board_lists()

    elif args['lb']:
        usecases.print_board_labels()

    elif args['l']:
        list_shortcuts = args['<list_shortcuts>']
        usecases.print_lists(list_shortcuts)

    elif args['g']:
        api_path = args['<api_path>']
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(tclient.get(api_path))

