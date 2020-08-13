import operator
import random
from collections import defaultdict

import stringdist

from sources.globals import GLOBAL_DATA
from sources.response_utils import gen_text_alco, gen_text_cocktail, get_suggests, get_suggests_cocktails
from sources.word_normalizer import norm


# приветсвтенное сообщение
def handle_new_session(req, res, tokens):
    if req['session']['new']:
        res['response']['card'] = {
            "type": "BigImage",
            "image_id": "997614/29e868d8ba3548bc33c8",
            "title": "Здравствуйте. Чем могу быть полезен?",
            "description": GLOBAL_DATA['HELP_TEXT'] + '\n\nСоздано при поддержке barclass.ru',
            "button": {
                "text": "Посетить сайт",
                "url": "http://barclass.ru",
                "payload": {}
            }
        }
        res['response']['text'] = GLOBAL_DATA['HELP_TEXT']
        res['response']['buttons'] = get_suggests(GLOBAL_DATA['START_SUGGEST'])
        return True
    return False


# запросы "что ты умеешь?", "помощь"
def handle_help(req, res, tokens):
    if "помощь" in tokens or ("что" in tokens and "ты" in tokens and "уметь" in tokens):
        res['response']['text'] = GLOBAL_DATA['HELP_TEXT_FULL']
        res['response']['buttons'] = get_suggests(GLOBAL_DATA['START_SUGGEST'])
        return True
    return False


# запросы "случайны рецепт" и т.д.
def handle_random_recipe(req, res, tokens):
    if ("коктейль" in tokens or "рецепт" in tokens) and (
            "какой" in tokens and "нибыть" in tokens or "случайный" in tokens
            or "рандомный" in tokens):
        res['response']['text'] = gen_text_cocktail(random.choice(list(GLOBAL_DATA['COCKTAILS'].keys())))
        res['response']['buttons'] = get_suggests(GLOBAL_DATA['START_SUGGEST'])
        return True
    return False


# запросы "что такое аперетив", "что такое бокал для шампанского" и т.д.
def handle_what_is(req, res, tokens):
    if "что" in tokens and "такой" in tokens or \
            "как" in tokens and "выглядеть" in tokens:
        filter(lambda t: t != "что" and t != "такой", tokens)
        for token in tokens:
            for d in GLOBAL_DATA['DICTIONARY']:
                for variant in d:
                    flag = False
                    if isinstance(variant, tuple):
                        flag = True
                        for word in variant:
                            if word[0] == '-':
                                if word in tokens:
                                    flag = False
                            else:
                                if word not in tokens:
                                    flag = False

                    elif variant == token:
                        flag = True

                    if flag:
                        if len(GLOBAL_DATA['DICTIONARY'][d]) == 1:
                            res['response']['text'] = GLOBAL_DATA['DICTIONARY'][d][0]
                            res['response']['buttons'] = get_suggests(GLOBAL_DATA['START_SUGGEST'])
                        elif len(GLOBAL_DATA['DICTIONARY'][d]) == 2:
                            res['response']['card'] = {
                                "type": "ItemsList",
                                "header": {
                                    "text": GLOBAL_DATA['DICTIONARY'][d][0] if GLOBAL_DATA['DICTIONARY'][d][0]
                                    else "Это легче показать, чем описать:",
                                },
                                "items": [
                                    {
                                        "title": "пример",
                                        "image_id": GLOBAL_DATA['DICTIONARY'][d][1]
                                    }
                                ]
                            }
                            if GLOBAL_DATA['DICTIONARY'][d][0]:
                                res['response']['text'] = GLOBAL_DATA['DICTIONARY'][d][0]
                            res['response']['buttons'] = get_suggests(GLOBAL_DATA['START_SUGGEST'])
                        return True
    return False


def handle_how_to_drink(req, res, tokens):
    if "пить" in tokens:
        tokens.remove("пить")
        for alco in GLOBAL_DATA['ALCO']:
            a_norm = norm(alco)
            for a in a_norm:
                if a in tokens:
                    res['response']['text'] = gen_text_alco(alco)
                    res['response']['buttons'] = get_suggests(["Коктейли с " + alco])
                    return True
    return False


def handle_cocktail_recipe(req, res, tokens):
    make_words = {"рецепт", "коктейль", "приготовить", "сделать", "изготовить", "создать"}
    if len(tokens.intersection(make_words)):
        for word in make_words:
            if word in tokens:
                tokens.remove(word)
        if "как" in tokens:
            tokens.remove("как")

        if "с" in tokens or "из" in tokens:
            if "сок" in tokens:
                tokens.remove("сок")
            answer = []
            wth = 'с'
            if wth in tokens or "из" in tokens:
                if wth in tokens:
                    tokens.remove(wth)
                if "из" in tokens:
                    tokens.remove("из")
                for token in tokens:
                    if token in GLOBAL_DATA['INGREDIENTS']:
                        answer += GLOBAL_DATA['INGREDIENTS'][token]
            if "без" in tokens:
                pass

            if len(answer) > 0:
                res['response']['text'] = gen_text_cocktail(answer[0])
                res['response']['buttons'] = get_suggests_cocktails(answer[1:5])
                return True

        else:
            result_list = defaultdict(float)
            for word in GLOBAL_DATA['COCKTAILS_WORDS']:
                for unit in GLOBAL_DATA['COCKTAILS_WORDS'][word]:
                    for token in tokens:
                        score = stringdist.levenshtein(word, token)
                        if score < 1:
                            score = 1
                        if score <= 8:
                            result_list[unit] += (1 / score) ** 2
            sorted_list = sorted(result_list.items(), key=operator.itemgetter(1), reverse=True)

            if sorted_list and sorted_list[0][1] > 0.25:
                res['response']['text'] = gen_text_cocktail(sorted_list[0][0])
                res['response']['buttons'] = get_suggests_cocktails(x[0] for x in sorted_list[1:5])
                return True
    return False


def handle_default(req, res, tokens):
    res['response']['text'] = 'Ничего не нашлось, давайте попробуем что-нибудь другое!' \
                              ' Для вызова справки скажите "помощь"'
    res['response']['buttons'] = get_suggests(GLOBAL_DATA['START_SUGGEST'])
    return True


REQUEST_HANDLERS = [
    handle_new_session,
    handle_help,
    handle_random_recipe,
    handle_what_is,
    handle_how_to_drink,
    handle_cocktail_recipe,
    handle_default
]