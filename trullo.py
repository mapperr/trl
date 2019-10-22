"""Trullo

Environment variables:

TRELLO_TOKEN
TRELLO_API_KEY

usage:
    trullo l
    trullo e <item-id>
    trullo d <item-id>
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
        res = tclient.get('/members/me/boards')
        counter = 1
        for item in res:
            for k, v in item.items():
                if k == 'name':
                    print(f'{counter} {v}')
            counter += 1
