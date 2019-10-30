import os
from typing import Dict, List

import attr
import requests

from trullo.trl_board import TrlBoard
from trullo.trl_card import TrlCard
from trullo.trl_list import TrlList


@attr.s(auto_attribs=True)
class TClient:
    trello_token: str = attr.ib(default=os.environ['TRELLO_TOKEN'] if 'TRELLO_TOKEN' in os.environ else '')
    trello_api_key: str = attr.ib(default=os.environ['TRELLO_API_KEY'] if 'TRELLO_API_KEY' in os.environ else '')
    base_url: str = attr.ib(default='https://api.trello.com/1')

    def build_auth_params(self) -> Dict[str, str]:
        return {'key': self.trello_api_key, 'token': self.trello_token}

    def get(self, path: str) -> Dict:
        return requests.get(self.base_url + path, self.build_auth_params()).json()

    def get_boards(self) -> List[TrlBoard]:
        res = self.get('/members/me/boards?lists=open')
        boards = list()
        for raw_board in res:
            board_id = ''
            board_closed = False
            for k, v in raw_board.items():
                if k == 'closed':
                    board_closed = v
                if k == 'id':
                    board_id = v
                if k == 'lists':
                    lists: List[TrlList] = self._extract_lists(v)
            if not board_closed:
                boards.append(TrlBoard(board_id, lists, raw_board))
        return boards

    def get_lists(self, board_id: str = None) -> List[TrlList]:
        if board_id is not None:
            return get_board_lists(board_id)

        boards = self.get_boards()
        lists = list()
        for board in boards:
           lists.append(board.lists)
        return lists

    def _extract_lists(self, raw_list: Dict) -> List[TrlList]:
        lists = list()
        for raw_data in raw_list:
            id_ = ''
            for k, v in raw_data.items():
                if k == 'id':
                    id_ = v
            lists.append(TrlList(id_, list(), raw_data))
        return lists

    def get_board_lists(self, board_id: str) -> List[TrlList]:
        api_path = f'/boards/{board_id}/lists'
        res = self.get(api_path)
        lists = list()
        for raw_data in res:
            id_ = ''
            for k, v in raw_data.items():
                if k == 'id':
                    id_ = v
            lists.append(TrlList(id_, list(), raw_data))
        return lists

    def get_cards(self, list_id: str = None) -> List[TrlCard]:
        api_path = '/members/me/cards'
        if list_id is not None:
            api_path = f'/lists/{list_id}/cards'
        res = self.get(api_path)
        cards = list()
        for raw_card in res:
            card_id = ''
            for k, v in raw_card.items():
                if k == 'id':
                    card_id = v
            cards.append(TrlCard(card_id, raw_card))
        return cards

    def get_card(self, card_id: str = None) -> TrlCard:
        api_path = f'/cards/{card_id}'
        res = self.get(api_path)
        return TrlCard(res['id'], res)

    def get_tree(self) -> List[TrlBoard]:
        cards = self.get_cards()
        boards = self.get_boards()

        for card in cards:
            for board in boards:
                for list_ in board.lists:
                    if card.raw_data['idList'] == list_.id:
                        list_.cards.append(card)

        return boards

