"""Trullo

usage:
    trl o
    trl b [<board_shortcut>]
    trl l n <list_name> [<after_list_shortcut>]
    trl l [<list_shortcuts>...]
    trl ll
    trl lb
    trl bm
    trl c <card_shortcut> [o | m <list_shortcut> | e | n <list_shortcut> | co [<comment>]]
    trl c n <list_shortcut>
    trl api <method_or_path> [<path>]
    trl -h

    -h --help  this help message


commands:
    o
        opens trello home in your browser
        or it opens the currently selected board in browser

    b [<board_shortcut>]
        shows the boards you can access
        with board_shortcut you can select the board you want to work with

    l [<list_shortcuts>...]
        shows lists and cards in the board you have currently selected
        with list_shortcuts you can show only selected lists and their cards

    l n <list_name> [<after_list_shortcut>]
        create a new list on the board

    ll
        shows only the board's lists

    lb
        shows the board's labels

    bm
        shows the board's members

    c <card_shortcut> [o | m <list_shortcut> | e | co [<comment>]]
        shows the card infos
        with o it opens the card shortUrl with your default browser
        with m and a target list you can move the card to that list
        with e you can edit the card title and description in your $EDITOR
        with co you can post a comment to the card (if omitted, opens your $EDITOR)

    c n <list_shortcut>
        create a new card in the list specified by list_shortcut

    api <method_or_path> [<path>]
        make a direct api call adding auth params automatically (for debugging/hacking purpose)
        method can be get/post/put/delete (default: get)
        Cf. https://developer.atlassian.com/cloud/trello/rest

env:
    you have to export this 2 variables to authenticate with trello:

    TRELLO_API_TOKEN - your trello api key
    TRELLO_TOKEN - a generated token

    you can obtain those values here: https://trello.com/app-key


trello development board: https://trello.com/b/fuK3ff2z

"""
import logging
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

    tmpdir = tempfile.gettempdir()
    selected_board_filepath = f'{tmpdir}/trl-selected-board'

    usecases = Usecases(TConfig(selected_board_filepath),
                        TClient(),
                        Normalizer(),
                        Printer())

    selected_board_id, selected_board_name = usecases.get_selected_board()

    if not args['b'] and selected_board_name is None:
        print(f'first select a board with `trl b`')
        exit(1)

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
            comment_command = args['co']
            if open_command:
                usecases.open_card_in_browser(card_shortcut)
            elif move_command:
                target_list_shortcut = args['<list_shortcut>']
                usecases.move_card(card_shortcut, target_list_shortcut)
            elif edit_command:
                usecases.update_card(card_shortcut)
            elif comment_command:
                comment = args.get('<comment>')
                usecases.comment_card(card_shortcut, comment)
            else:
                usecases.print_card(card_shortcut)

    elif args['b']:
        if args['<board_shortcut>']:
            board_shortcut = args['<board_shortcut>']
            usecases.select_board(board_shortcut)
        else:
            usecases.print_board_list()

    elif args['o']:
        board_id, board_name = usecases.get_selected_board()
        if board_id is None:
            usecases.open_trello_in_browser()
        else:
            usecases.open_selected_board_in_browser()

    elif args['ll']:
        usecases.print_board_lists()

    elif args['lb']:
        usecases.print_board_labels()

    elif args['bm']:
        usecases.print_board_members()

    elif args['l']:
        breakpoint()
        new_command = args['n']
        if new_command:
            list_name = args['<list_name>']
            after_list_shortcut = args.get('<after_list_shortcut>')
            usecases.create_list(list_name, after_list_shortcut)
        else:
            list_shortcuts = args['<list_shortcuts>']
            usecases.print_lists(list_shortcuts)

    elif args['api']:
        api_path = args.get('<path>')
        if api_path is None:
            api_path = args["<method_or_path>"]
            method = "get"
        else:
            method = args["<method_or_path>"]
        usecases.run_api_request(method=method, path=api_path)
