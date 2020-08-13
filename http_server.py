# -*- coding: utf-8 -*-
import json
import logging
from api import handle_dialog
from flask import Flask, request
app = Flask(__name__)


@app.route("/", methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


if __name__ == "__main__":
    app.run(ssl_context='adhoc', host='0.0.0.0', port=8080)
