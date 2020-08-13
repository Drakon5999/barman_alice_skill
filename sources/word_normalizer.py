import pymorphy2

MORPH = pymorphy2.MorphAnalyzer(lang='ru')


def norm(x):
    p = MORPH.parse(x)
    return list(t.normal_form for t in p)