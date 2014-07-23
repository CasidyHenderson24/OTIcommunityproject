#!/usr/bin/env python

import requests
from lxml import html
import gzip
from StringIO import StringIO

listname = 'commotion-discuss'
url = 'https://lists.chambana.net/pipermail/' + listname + '/'

response = requests.get(url)
tree = html.fromstring(response.text)

filenames = tree.xpath('//table/tr/td[3]/a/@href')

def emails_from_filename(filename):
    print filename
    response = requests.get(url + filename)
    if filename[-3:] == '.gz':
        contents = gzip.GzipFile(fileobj=StringIO(response.content)).read()
    else:
        contents = response.content
    return contents

contents = [emails_from_filename(filename) for filename in filenames]
contents.reverse()

contents = "\n\n\n\n".join(contents)

with open(listname + '.txt', 'w') as filehandle:
    filehandle.write(contents)
