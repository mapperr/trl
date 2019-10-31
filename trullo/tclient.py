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

    def put(self, path: str) -> Dict:
        return requests.put(self.base_url + path, self.build_auth_params()).json()

    def get_boards(self) -> List[TrlBoard]:
        res = self.get('/members/me/boards?lists=open')
        boards = list()
        for raw_board in res:
            board_id = ''
            board_closed = False
            lists: List[TrlList] = []
            for k, v in raw_board.items():
                if k == 'closed':
                    board_closed = v
                if k == 'id':
                    board_id = v
                if k == 'lists':
                    lists = self._extract_lists(v)
            if not board_closed:
                boards.append(TrlBoard(board_id, raw_board['shortLink'], lists, [], raw_board))
        return boards

    def get_board(self, board_id: str) -> TrlBoard:
        res = self.get(f'/batch?urls=/board/{board_id},/board/{board_id}/lists/open,/board/{board_id}/cards/open')
        board = TrlBoard(board_id, board_id, [], [], res[0]['200'])
        for item in res[1]['200']:
            list_ = TrlList(item['id'], item)
            board.lists.append(list_)
        for item in res[2]['200']:
            card = TrlCard(item['id'], item['shortLink'], item)
            board.cards.append(card)
        return board

    def _extract_lists(self, raw_list: Dict) -> List[TrlList]:
        lists = list()
        for raw_data in raw_list:
            id_ = ''
            for k, v in raw_data.items():
                if k == 'id':
                    id_ = v
            lists.append(TrlList(id_, raw_data))
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
            lists.append(TrlList(id_, raw_data))
        return lists

    def get_cards(self, list_id: str = None) -> List[TrlCard]:
        api_path = '/members/me/cards'
        if list_id is not None:
            api_path = f'/lists/{list_id}/cards'
        res = self.get(api_path)
        return self._extract_cards(res)

    def _extract_cards(self, raw_list: Dict) -> List[TrlCard]:
        cards = list()
        for raw_card in raw_list:
            card_id = ''
            for k, v in raw_card.items():
                if k == 'id':
                    card_id = v
            cards.append(TrlCard(card_id, raw_card['shortLink'], raw_card))
        return cards

    def get_card(self, card_id: str = None) -> TrlCard:
        api_path = f'/cards/{card_id}'
        res = self.get(api_path)
        return TrlCard(res['id'], res['shortLink'], res)

    def move_card(self, card_id: str, list_id: str, board_id: str = None):
        api_path = f'/cards/{card_id}?idList={list_id}'
        if board_id is not None:
            api_path += f'&idBoard={board_id}'
        self.put(api_path)

    def edit_card(self, card_id: str, name: str = None, desc: str = None):
        api_path = f'/cards/{card_id}?'
        if name is not None:
            api_path += '' if api_path.endswith('?') else '&'
            api_path += f'name={name}'
        if desc is not None:
            api_path += '' if api_path.endswith('?') else '&'
            api_path += f'desc={desc}'
        self.put(api_path)
