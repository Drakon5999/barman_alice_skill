from sources.globals import GLOBAL_DATA


def gen_text_cocktail(key):
    text = ''
    ct = GLOBAL_DATA['COCKTAILS'][key]
    text += "{name} - {name_en}\n Категория: {category}\n".format(**ct)
    for ingr in ct['ingredients']:
        if ct['ingredients'][ingr]:
            text += "-" + ingr + ": " + ct['ingredients'][ingr] + "\n"
        else:
            text += "-" + ingr + "\n"
    text += "\n"
    text += "{additional}\n\n{recept}".format(**ct)
    return text


def gen_text_alco(key):
    ct = GLOBAL_DATA['ALCO'][key]
    text = ct[0] + "\n\n"
    if ct[1]:
        text += "Хорошо сочетается: " + ct[1].lower()
    return text


def get_suggests(names):
    suggests = []
    for name in names:
        suggests.append({
            "title": name,
            # "url": "",
            "hide": True
        })

    return suggests


def get_suggests_cocktails(names):
    return get_suggests(GLOBAL_DATA['COCKTAILS'][x]['name'] for x in names)