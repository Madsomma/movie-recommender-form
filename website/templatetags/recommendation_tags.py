from django import template
import json


register = template.Library()


@register.filter(name='explanation_genre')
def explanation_genre(string, arg):
    string = string.replace('\'', '"')
    dic = json.loads(string)
    dic_list = list(dic.items())
    return dic_list[int(arg)][0]


@register.filter(name='explanation_number')
def explanation_number(string, arg):
    string = string.replace('\'', '"')
    dic = json.loads(string)
    dic_list = list(dic.items())
    return dic_list[int(arg)][1]
