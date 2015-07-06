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
	print request.url_root
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

	args = {'exhibition_id': ex_id, 'has_images': '1', 'page':'1', 'per_page':'100'}
	rsp = api.execute_method('cooperhewitt.exhibitions.getObjects', args)

	# 	retrieving exhibition info through another api	w/ exhibition id		
	args = {'exhibition_id': ex_id}
	rsp2 = api.execute_method('cooperhewitt.exhibitions.getInfo', args)

	data = rsp['objects']

	i=0
	for item in data:
		
		obj_id = item['id']
		args = {'object_id': obj_id, 'page':'1', 'per_page':'100'}
		tags = api.execute_method('cooperhewitt.objects.tags.getTags', args)
		
		data[i]['tags'] = tags['tags']
				
		i = i + 1
	
	return render_template('obj_page.html',
							data=data,
							rsp2=rsp2)
	

if __name__ == "__main__":
	### note: this is setup for a local config. need to add proper settings for heroku ( MJW/20150701 )
    app.run()