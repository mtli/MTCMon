from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys, os

from flask import Flask
from flask import send_from_directory
from flask import render_template

node_list = open('node-list.txt').readlines()
node_list = [x.strip() for x in node_list] 
if not os.path.isdir('nodestats'):
    os.makedirs('nodestats')

app = Flask(__name__, static_url_path='')

@app.route('/')
@app.route('/gpus.html') # for backward compatibility
def root():
    sections = [None]*len(node_list)
    for i, node in enumerate(node_list):
        try:
            sections[i] = open('nodestats/' + node + '.html').read()
        except Exception as e:
            print(e)
            sections[i] = render_template('section-error.html', machine_name=node)
    return render_template('index.html', sections=sections)

@app.route('/static/<path:path>')
def sendui(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    port = 50692 if len(sys.argv) < 2 else int(sys.argv[1])
    app.run('0.0.0.0', port, threaded=True)
