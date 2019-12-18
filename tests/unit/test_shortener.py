import unittest
from typing import List
from unittest import mock
from unittest.mock import Mock

from trullo.normalizer import Normalizer
from trullo.shortcuttable import Shortcuttable
from trullo.trl_board import TrlBoard
from trullo.trl_card import TrlCard
from trullo.trl_label import TrlLabel
from trullo.trl_list import TrlList


class TestShortener(unittest.TestCase):
    def test_matches(self):
        sh = Normalizer
        start_match = sh.is_a_match('pil', 'pillow')
        self.assertTrue(start_match)
        middle_match = sh.is_a_match('grat', 'integration')
        self.assertTrue(middle_match)
        end_match = sh.is_a_match('ver', 'forever')
        self.assertTrue(end_match)

    def test_wrong_matches(self):
        sh = Normalizer
        match = sh.is_a_match('spil', 'pillow')
        self.assertFalse(match)

    def test_matches_in_list(self):
        short1: Shortcuttable = \
            mock.create_autospec(Shortcuttable, spec_set=True)
        short1.get_normalized_name = Mock(return_value='qwerty')
        short2: Shortcuttable = \
            mock.create_autospec(Shortcuttable, spec_set=True)
        short2.get_normalized_name = Mock(return_value='asdfgh')
        short3: Shortcuttable = \
            mock.create_autospec(Shortcuttable, spec_set=True)
        short3.get_normalized_name = Mock(return_value='qwertyasdfgh')
        short4: Shortcuttable = \
            mock.create_autospec(Shortcuttable, spec_set=True)
        short4.get_normalized_name = Mock(return_value='')

        sh = Normalizer
        shorties = [short1, short2]
        matches: List = sh.get_matches('er', shorties)
        self.assertEqual(1, len(matches))
        matches: List = sh.get_matches('df', shorties)
        self.assertEqual(1, len(matches))
        matches: List = sh.get_matches('mn', shorties)
        self.assertEqual(0, len(matches))
        matches: List = sh.get_matches('rty', shorties + [short3])
        self.assertEqual(2, len(matches))
        matches: List = sh.get_matches('er', shorties + [short4])
        self.assertEqual(1, len(matches))

    def test_normalization(self):
        card1 = TrlCard('idc1', shortLink := 'qWeRt1',
                        {'name': 'Design the project in 2 days',
                         'shortLink': shortLink})
        card2 = TrlCard('idc2', shortLink := 'AsD3gH',
                        {'name': 'Produce a non-techical doc, clear and easy',
                         'shortLink': shortLink})
        card3 = TrlCard('idc3', shortLink := 'zXcvb7',
                        {'name': ' Implement a trim() function',
                         'shortLink': shortLink})
        list1 = TrlList('idl1', {'name': 'To Do'})
        label1 = TrlLabel('idlb1', lblname := 'feature',
                          {'name': lblname, 'color': 'blue'}, 'blue')
        board1 = TrlBoard('idb1', shortLink := 'p01UyT', [list1],
                          [card1, card2, card3], [label1],
                          {'name': 'my Super Board',
                           'shortLink': shortLink})

        card1_n = card1.get_normalized_name()
        self.assertNotIn('D', card1_n)
        self.assertNotIn(' ', card1_n)
        self.assertIn('2', card1_n)
        self.assertIn('project', card1_n)
        self.assertIn('design', card1_n)
        self.assertIn('days', card1_n)

        card2_n = card2.get_normalized_name()
        self.assertNotIn('P', card2_n)
        self.assertNotIn(' ', card2_n)
        self.assertNotIn('-', card2_n)
        self.assertNotIn(',', card2_n)
        self.assertIn('nontech', card2_n)
        self.assertIn('docclear', card2_n)
        self.assertIn('produce', card2_n)

        card3_n = card3.get_normalized_name()
        self.assertNotIn('I', card3_n)
        self.assertNotIn(' ', card2_n)
        self.assertNotIn(' impl', card3_n)
        self.assertNotIn('(', card3_n)
        self.assertIn('trimfunc', card3_n)

        list1_n = list1.get_normalized_name()
        self.assertNotIn('T', list1_n)
        self.assertNotIn(' ', list1_n)
        self.assertIn('idl1', list1_n)
        self.assertIn('todo', list1_n)

        board1_n = board1.get_normalized_name()
        self.assertNotIn(' ', board1_n)
        self.assertNotIn('U', board1_n)
        self.assertIn('mysuper', board1_n)
        self.assertIn('p01u', board1_n)
