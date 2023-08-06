"""Very helpful for noobs"""

import random
import requests
import os

def rdn_text(chars, quantia):
    return "".join(random.choice(chars) for i in range(quantia))

def get_url_text(url):
    request = requests.get(url)
    return request.text

def get_file_content(file):
    return open(file, "r").read()

def simple_create_file(file, content):
    return open(file, "w+").write(content)

def list_to_string(alist):
    return "".join(alist)

def choose_random_element_from_array(array):
    return random.choice(array)

def simple_delete_file(file):
    return os.remove(file)