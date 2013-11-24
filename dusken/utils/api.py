import string
import random
from django.utils.text import slugify

def random_string(max_length=15):
    return u''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(max_length))

def generate_username(data, max_length=15):
    username = u""
    # 1. join first and last name
    username = u"{}{}".format(
        slugify(data.get('first_name', u'')),
        slugify(data.get('last_name', u'')))
    if not username:
        # 2. if no first and last, generate random
        # TODO set flag so that unspecified username can be cheched later
        username = random_string(max_length)

    return username
