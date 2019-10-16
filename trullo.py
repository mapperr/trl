"""Trullo

Environment variables:

TRELLO_TOKEN
TRELLO_API_KEY

usage:
    trullo l
    trullo e <item-id>
    trullo d <board-id>
    trullo c (<c> | <l> | <b>)

    -h --help this help message
    -v --version print version and exit

"""
from docopt import docopt

from trullo.tclient import TClient

if __name__ == '__main__':
    args = docopt(__doc__, version='Trullo beta')

    tclient = TClient()

    if args['l']:
        print(tclient.get('/members/me/boards'))

