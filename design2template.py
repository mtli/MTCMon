from __future__ import absolute_import

import re
from os import makedirs
from os.path import join, dirname, isdir
import io # for python2.7

abs_path = dirname(__file__)
in_file = join(abs_path, 'index-design.html')                                                                             
out_dir = join(abs_path, 'templates')
out_file = 'index.html'

use_toc = True
node_list = 'node-list.txt'


if not isdir(out_dir):
	makedirs(out_dir)

with io.open(in_file, encoding='utf8') as fin:
	content = fin.read()

if use_toc:
	node_list = io.open('node-list.txt', encoding='utf8').readlines()
	node_list = [x.strip() for x in node_list] 

	node_list_html = '	<ul>\n'
	for node in node_list:
		node_list_html += \
			'		<li><a class="scroll-to" href="#%s">%s</a></li>\n' % \
				(node, node)
	node_list_html += '	</ul>\n'
	content = re.sub('<!-- Index List Start -->.*?<!-- Index List End -->', node_list_html, content, flags = re.DOTALL)
else:
	content = re.sub('<!-- ToC Start -->.*?<!-- ToC End -->', '', content, flags = re.DOTALL)

sections = '{% for section in sections %}\n{{ section|safe }}\n{% endfor %}'
content = re.sub('<!-- Content Start -->.*?<!-- Content End -->', sections, content, flags = re.DOTALL)

with io.open(join(out_dir, out_file), 'w', encoding='utf8') as fout:
    fout.write(content)
