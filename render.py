from __future__ import absolute_import                                                                                 
from __future__ import division
from __future__ import print_function

import sys, os, io
# io is for python2 with UTF-8 support
from time import sleep
from flask import Flask
from flask import render_template

abs_path = os.path.dirname(__file__)
web_path = os.path.join(abs_path, 'share/web/')
nodestats = ('/project_data/mtcmon/nodestats/')
node_list = os.path.join(abs_path, 'node-list.txt')
node_list = open(node_list).readlines()
node_list = [x.strip() for x in node_list]
app = Flask('Dummy Flask', root_path=abs_path)

if not os.path.isdir(web_path):
       os.makedirs(web_path)
       os.symlink('/opt/MTCMon/static', '/opt/MTCMon/share/web/static')

def main():
  sections = [None]*len(node_list)
  with app.app_context():
    while 1:
      for i, node in enumerate(node_list):
        try:
          sections[i] = open(nodestats + node + '.html').read()
        except Exception as e:
          print(e)
          sections[i] = render_template('section-error.html', machine_name=node)
      html = render_template('index.html', sections=sections)
      io.open(os.path.join(web_path + '/index.html'), 'w', encoding='utf8').write(html)
      sleep(30)

if __name__ == "__main__":
    main()
