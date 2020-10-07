from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import io # for python2.7

abs_path = os.path.dirname(__file__)
in_file = abs_path + '/index-design.html'                                                                              
out_dir = abs_path + '/templates'
out_file = 'index.html'

if not os.path.isdir(out_dir):
  os.makedirs(out_dir)
  
with io.open(in_file, encoding='utf8') as fin:
  content = fin.read()
  
sections = '{% for section in sections %}\n{{ section|safe }}\n{% endfor %}'
content = re.sub('<!-- Content Start -->.*?<!-- Content End -->', sections, content, flags = re.DOTALL)

with io.open(os.path.join(out_dir, out_file), 'w', encoding='utf8') as fout:
    fout.write(content)

