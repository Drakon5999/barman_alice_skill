# -*- coding: utf-8 -*-
import unittest
from api import handle_dialog
from sources.globals import GLOBAL_DATA
from test_utils import make_request, make_response


class TestDialog(unittest.TestCase):
    def test_init(self):
        request = make_request('', True)
        response = make_response()
        handle_dialog(request, response)
        self.assertEqual(GLOBAL_DATA['HELP_TEXT'], response['response']['text'])
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_recipe(self):
        request = make_request('рецепт кровавой мэри')
        response = make_response()
        handle_dialog(request, response)
        self.assertIn("кровавая мэри", response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_how_to_drink(self):
        request = make_request('как пить джин')
        response = make_response()
        handle_dialog(request, response)
        self.assertIn(GLOBAL_DATA['ALCO']['джин'][0].lower(), response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_cocktails_with(self):
        request = make_request('коктейли с джин')
        response = make_response()
        handle_dialog(request, response)
        self.assertIn('джин', response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_what_is(self):
        request = make_request('что такое аперитив')
        response = make_response()
        handle_dialog(request, response)
        self.assertIn(GLOBAL_DATA['DICTIONARY'][("аперитив",)][0].lower(), response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_default(self):
        request = make_request('asdfaaa')
        response = make_response()
        handle_dialog(request, response)
        self.assertIn("ничего не нашлось", response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_what_is__multiword(self):
        request = make_request('что такое бокал для шампанского')
        response = make_response()
        handle_dialog(request, response)
        self.assertIn("это легче показать, чем описать", response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_cocktail_single_word(self):
        request = make_request('авиация')
        response = make_response()
        handle_dialog(request, response)
        self.assertIn("авиация", response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)


if __name__ == '__main__':
    unittest.main()
