#!/usr/bin/env python
#encoding=utf-8

import sys
from flask import Flask, render_template, request, url_for
import json

sys.path.append(".")
from DataGene.k_net_model import *
city_num=10

print("import sucess!")

# get solver dictionary
x_dict = opt_solve() 

x_dict_keys = list(x_dict.keys())

all_dict1 = {}
all_dict2 = {}
for i in range(city_num):
    for j in range(city_num):
        keyword=str(i)+"-"+str(j)
        all_dict1[keyword]=[]
        all_dict2[keyword]=[]

for tag_tuple in x_dict:
    if(tag_tuple[4]==0 and abs(x_dict[tag_tuple]-1)<0.5):
        keyword = str(tag_tuple[2])+"-"+str(tag_tuple[3])
        value = [tag_tuple[0],tag_tuple[1]]
        all_dict1[keyword].append(value)

for tag_tuple in x_dict:
    if(tag_tuple[4]==1 and abs(x_dict[tag_tuple]-1)<0.5):
        keyword = str(tag_tuple[2])+"-"+str(tag_tuple[3])
        value = [tag_tuple[0],tag_tuple[1]]
        all_dict2[keyword].append(value)

print(all_dict1)
# print(all_dict2)
# print(x_dict)