from api import handle_dialog
from test_utils import make_request, make_response
from pprint import pprint


def main():
    request = make_request('', True)
    response = make_response()
    handle_dialog(request, response)
    pprint(response['response'])
    while True:
        phrase = input()
        request = make_request(phrase.lower())
        response = make_response()
        handle_dialog(request, response)
        pprint(response['response'])


if __name__ == '__main__':
    main()