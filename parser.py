# coding=utf-8
from lxml import html
from urllib.request import urlopen
import json
import re

response = urlopen("https://barclass.ru/glossary/coctails/official-iba.php")
parsed_body = html.fromstring(response.read())
links = parsed_body.xpath('/html/body/div/div[3]/div[1]/p/a/@href')
links1 = parsed_body.xpath('/html/body/div/div[3]/div[2]/p/a/@href')
links2 = parsed_body.xpath('/html/body/div/div[3]/div[3]/p/a/@href')
links3 = parsed_body.xpath('/html/body/div/div[3]/div[4]/p/a/@href')
all = list(links) + list(links1) + list(links2) + list(links3)

drinks = dict()

for link in all:
    url = "https://barclass.ru" + link
    response = urlopen(url)
    parsed_body = html.fromstring(response.read().decode('CP1251'))
    name = str(parsed_body.xpath('/html/body/div/h1')[0].text_content())
    name = name.replace('–', '-')
    name = name.split(' - ')
    print(name)

    category = str(parsed_body.xpath('/html/body/div/div[3]/div[2]/h3')[0].text_content())
    category = category.split(": ")

    ingredients = parsed_body.xpath('/html/body/div/div[3]/div[2]/ul')[0]
    ingr_dict = dict()
    for ingr in ingredients.getchildren():
        ingr = ingr.text_content().split(" - ")
        if len(ingr) == 1:
            ingr.append("")
        ingr_dict[ingr[0]] = ingr[1]

    additional = str(parsed_body.xpath('/html/body/div/div[3]/div[2]/p[1]')[0].text_content()).split("\n")
    additional = "\n".join(x.strip() for x in additional)
    additional = additional.strip()

    recept = str(parsed_body.xpath('/html/body/div/div[3]/div[2]/p[2]')[0].text_content())

    cocktail_data = dict()
    cocktail_data["name"] = name[0].strip() # russian name
    cocktail_data["name_en"] = name[1].strip() # russian name
    cocktail_data["category"] = category[1].strip() # category name
    cocktail_data["ingredients"] = ingr_dict
    cocktail_data["additional"] = additional # method, glass, garnere
    cocktail_data["recept"] = recept # method, glass, garnere


    drinks[name[0].lower().strip()] = cocktail_data

with open("dumped.json", "w") as dmpf:
    json.dump(drinks, dmpf)
