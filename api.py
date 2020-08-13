# -*- coding: utf-8 -*-
import logging
from sources.word_normalizer import norm
from sources.request_handlers import REQUEST_HANDLERS

logging.basicConfig(level=logging.DEBUG)


def handle(event, context):
    if 'request' in event:
        logging.info('Request: %r', event)

        response = {
            "version": event['version'],
            "session": event['session'],
            "response": {
                "end_session": False
            }
        }

        handle_dialog(event, response)

        logging.info('Response: %r', response)

        return response

    return {}


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    tokens = set(norm(x)[0] for x in req['request']['nlu']['tokens'])

    for handler in REQUEST_HANDLERS:
        if handler(req, res, tokens):
            return
