from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, os, io
# io is for python2 with UTF-8 support
from time import sleep

from flask import Flask
from flask import render_template

app = Flask('Dummy Flask')

node_list = open('node-list.txt').readlines()
node_list = [x.strip() for x in node_list] 

def main():
    sections = [None]*len(node_list)
    with app.app_context():
        while 1:
            for i, node in enumerate(node_list):
                try:
                    sections[i] = open('/project_data/MTCMon/nodestats/' + node + '.html').read()
                except Exception as e:
                    print(e)
                    sections[i] = render_template('section-error.html', machine_name=node)
            html = render_template('index.html', sections=sections)
            io.open('/opt/MTCMon/share/web/index.html', 'w', encoding='utf8').write(html)
            sleep(30)

if __name__ == "__main__":
    main()