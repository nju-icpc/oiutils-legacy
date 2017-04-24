from pkg_resources import resource_stream, Requirement
from flask import Flask, render_template, jsonify, url_for
from flask import render_template_string
from flask import escape
from flask import Markup
import sys, os
import time

app = Flask(__name__)

@app.route('/')
def index():
    fp = resource_stream(
             Requirement.parse("oiutils>=0.1"),
             "oi/visual/templates/index.html"
         )
    jquery_fp = resource_stream(
                    Requirement.parse("oiutils>=0.1"), 
                    "oi/visual/static/js/jquery.js"
                )
    oi_fp = resource_stream(
                Requirement.parse("oiutils>=0.1"),
                "oi/visual/static/js/oi.js"
            )
    tablecss_fp = resource_stream(
                Requirement.parse("oiutils>=0.1"),
                "oi/visual/static/css/table.css"
            )
    fp_c = fp.read()
    jquery_c = jquery_fp.read()
    oi_c = oi_fp.read()
    tablecss_c = tablecss_fp.read()

    fp.close()
    jquery_fp.close()
    oi_fp.close()
    tablecss_fp.close()
    return render_template_string(
                fp_c, 
                content='helloworld', 
                jquery_code=Markup(jquery_c),
                oi_code=Markup(oi_c),
                tablecss_code=Markup(tablecss_c),
            )

@app.route('/get_ranklist')
def get_ranklist():
    try:
        fp = open(os.path.join(os.getcwd(), 'oi.log'), 'r')
        return jsonify(result = fp.read())
    except:
        print('log file does not exist')
        return jsonify(result = "") 

def oi_visual(argv):
    app.run()

if __name__ == '__main__':
    app.run()
