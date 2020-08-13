# -*- coding: utf-8 -*-
from collections import defaultdict
import json

from term_database import ALCO, DICTIONARY
from word_normalizer import norm

GLOBAL_DATA = {
    'COCKTAILS': {},
    'COCKTAILS_WORDS': defaultdict(list),
    'INGREDIENTS': defaultdict(list),
    'HELP_TEXT': 'Я умею подсказать рецепты коктейлей из списка IBA,' \
                 ' коктейль с каким-нибудь ингридиентом,' \
                 ' как правильно пить алкогольные напитки в чистом виде и значения разных терминов.',
    'HELP_TEXT_FULL': 'Коктейли я могу искать по названию или его части.' \
                      '\nЕсли хотите найти коктейли с абсентом спросите "коктейль с абсентом",' \
                      ' вместо абсента можете подставить свой ингридиент.' \
                      '\nЕсли значение какого-либо термина вам не знакомо, можете спросить меня "что такое *термин*?",' \
                      ' и я постараюсь ответить' \
                      '\nТакже вы можете спросить меня о том, как пить водку, ром, джин и другие алкогольные напитки в чистом виде.',

    'START_SUGGEST': ["Как пить Джин?", "Рецепт Кровавой Мэри", "Коктейль с абсентом", "Что такое аперитив?"],
    'ALCO': ALCO,
    'DICTIONARY': DICTIONARY
}


with open("dumped_cocktails.json", "r", encoding="utf8") as dc:
    GLOBAL_DATA['COCKTAILS'] = json.load(dc)

for cocktail in GLOBAL_DATA['COCKTAILS']:
    words = cocktail.split(' ')
    for word in words:
        for n in norm(word.lower()):
            if cocktail not in GLOBAL_DATA['COCKTAILS_WORDS'][n]:
                GLOBAL_DATA['COCKTAILS_WORDS'][n].append(cocktail)
for cocktail in GLOBAL_DATA['COCKTAILS']:
    for ingr in GLOBAL_DATA['COCKTAILS'][cocktail]["ingredients"]:
        words = ingr.split(' ')
        for word in words:
            for n in norm(word.lower()):
                if cocktail not in GLOBAL_DATA['INGREDIENTS'][n]:
                    GLOBAL_DATA['INGREDIENTS'][n].append(cocktail)
