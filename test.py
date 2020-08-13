# -*- coding: utf-8 -*-
import unittest
from collections import defaultdict
from api import handle_dialog
from sources.globals import GLOBAL_DATA


def make_request(phrase, is_new=False):
    return {
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
            "interfaces": {
                "screen": {},
                "payments": {},
                "account_linking": {}
            }
        },
        "session": {
            "message_id": 0,
            "session_id": "0ab0148e-ca4e-4452-9ebc-9d4861be91b6",
            "skill_id": "dcb1af57-30e1-499f-b7fd-6d4a640d877f",
            "user": {
                "user_id": "150698BA642B3A71DFCCADB6EEB8D3480E33994093336ED74B823B2CC2BBB780"
            },
            "application": {
                "application_id": "19CD0F51B2836F8B4FB7106683CC9414912695363E6BB213E4D36C84291D99DF"
            },
            "new": is_new,
            "user_id": "19CD0F51B2836F8B4FB7106683CC9414912695363E6BB213E4D36C84291D99DF"
        },
        "request": {
            "command": phrase,
            "original_utterance": phrase,
            "nlu": {
                "tokens": phrase.split(),
                "entities": [],
                "intents": {}
            },
            "markup": {
                "dangerous_context": False
            },
            "type": "SimpleUtterance"
        },
        "version": "1.0"
    }


class TestDialog(unittest.TestCase):
    def test_init(self):
        request = make_request('', True)
        response = defaultdict(dict)
        handle_dialog(request, response)
        self.assertEqual(GLOBAL_DATA['HELP_TEXT'], response['response']['text'])
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_recipe(self):
        request = make_request('рецепт кровавой мэри')
        response = defaultdict(dict)
        handle_dialog(request, response)
        self.assertIn("кровавая мэри", response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_how_to_drink(self):
        request = make_request('как пить джин')
        response = defaultdict(dict)
        handle_dialog(request, response)
        self.assertIn(GLOBAL_DATA['ALCO']['джин'][0].lower(), response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_cocktails_with(self):
        request = make_request('коктейли с джин')
        response = defaultdict(dict)
        handle_dialog(request, response)
        self.assertIn('джин', response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_what_is(self):
        request = make_request('что такое аперитив')
        response = defaultdict(dict)
        handle_dialog(request, response)
        self.assertIn(GLOBAL_DATA['DICTIONARY'][("аперитив",)][0].lower(), response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)

    def test_default(self):
        request = make_request('asdf')
        response = defaultdict(dict)
        handle_dialog(request, response)
        self.assertIn("ничего не нашлось", response['response']['text'].lower())
        self.assertGreater(len(response['response']['buttons']), 0)


if __name__ == '__main__':
    unittest.main()
