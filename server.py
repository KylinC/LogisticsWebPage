#!/usr/bin/env python
#encoding=utf-8

import sys
from flask import Flask, render_template, request, url_for, Response
import json
# from neo4j import GraphDatabase
from DataSet.locations import get_json_data
from DataSet.relationship import get_route_data

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',result=404)

@app.route('/data')
def data():
    callback = request.args.get('callback')
    json_data = get_json_data()
    return Response('{}({})'.format(callback, json_data))

@app.route('/allroute',methods=['POST','GET'])
def allroute():
    callback = request.args.get('callback')
    json_data = get_route_data()
    return Response('{}({})'.format(callback, json_data))

if __name__ == "__main__":
    app.run(debug = True)