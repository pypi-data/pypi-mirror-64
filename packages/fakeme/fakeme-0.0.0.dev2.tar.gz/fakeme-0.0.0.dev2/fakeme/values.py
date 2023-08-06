
import string
import random  # noqa F401
import re  # noqa F401
from uuid import uuid1, uuid4  # noqa F401
from random import randint, random, choice, choices  # noqa F401


from mimesis import Generic, Datetime, Text, Address, Person


languages = ['zh', 'ru', 'en', 'es', 'ar', 'fr']


fake = Generic()
text = Text()
person = Person()
date = Datetime()
address = Address()


current_time = None
last_time = None


def random_char(_len):
    return ''.join([choice(string.ascii_letters) for x in range(_len)]).upper()


def values_generator(rule=None):
    """ values generator, that eval rules what was defined in 'generator' key  """

    value = None
    if rule and rule['generator']:
        value = eval(rule['generator'])
        if rule.get('len', '') and isinstance(rule['len'], int):
            value = value[0:rule['len']]
    return value
