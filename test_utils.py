from collections import defaultdict


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


def make_response():
    return defaultdict(dict)