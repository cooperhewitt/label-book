#!/usr/bin/env python

from sys import argv
import json
import cooperhewitt.api.client
import os
import urllib


CH_ACCESS_TOKEN = os.environ['CH_ACCESS_TOKEN']

## adding flask here ( MJW/20150701 )
from flask import Flask, request
from flask import render_template
app = Flask(__name__)

#

@app.route("/")
def home():
	api = cooperhewitt.api.client.OAuth2(CH_ACCESS_TOKEN)

	## retreiving data from api to get list of exhibitions ( ATG/20150705 )
	args = {'page':'1', 'per_page':'100'}
	rsp4 = api.execute_method('cooperhewitt.exhibitions.getList', args)

	return render_template('index.html',
							rsp4=rsp4)

#

@app.route("/<int:ex_id>")
def exhibitiion(ex_id):
	return build_page(ex_id)

def build_page(ex_id):
	api = cooperhewitt.api.client.OAuth2(CH_ACCESS_TOKEN)

	# 	retrieving exhibition info through another api	w/ exhibition id		
	args = {'exhibition_id': ex_id}
	rsp2 = api.execute_method('cooperhewitt.exhibitions.getInfo', args)

	
	args = {'exhibition_id': ex_id, 'has_images': '1', 'page':'1', 'per_page':'100'}
	rsp = api.execute_method('cooperhewitt.exhibitions.getObjects', args)

	data = rsp['objects']
	for item in data:
		
		obj_id = item['id']

		args = {'object_id': obj_id, 'page':'1', 'per_page':'100'}
		tagsarray = api.execute_method('cooperhewitt.objects.tags.getTags', args)

		item['tags'] = tagsarray['tags']

		args = {'object_id': obj_id, 'page':'1', 'per_page':'100'}
		locationarray = api.execute_method('cooperhewitt.objects.isOnDisplay', args)
		
		item['locationinfo'] = locationarray
				
	return render_template('obj_page.html',
							data=data,
							rsp2=rsp2)
	

if __name__ == "__main__":
	app.run()
