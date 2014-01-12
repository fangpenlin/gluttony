import os
import re

import pandoc

pandoc.core.PANDOC_PATH = os.environ['PANDOC_PATH']

doc = pandoc.Document()
with open('README.md', 'rt') as md:
    doc.markdown = md.read()
    with open('README.txt', 'wt') as rst:
        rst_txt = doc.rst
        rst_txt = rst_txt.replace('\r\n', '\n')
        rst_txt = re.sub(r':alt: (.*)\n(\s+)(.*)', r':alt: \1\n', rst_txt)
        rst.write(rst_txt)

print 'done'
