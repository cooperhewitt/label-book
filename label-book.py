#!/usr/bin/env python

from sys import argv
import json
#import cooperhewitt.api.client
import os
import urllib
import pprint

# For parallel processing via aaron
import cooperhewitt.api.multiclient 

CH_ACCESS_TOKEN = os.environ['CH_ACCESS_TOKEN']

## adding flask here ( MJW/20150701 )
from flask import Flask, request
from flask import render_template
app = Flask(__name__)
#



@app.route("/")
def home():
	api = cooperhewitt.api.multiclient.OAuth2(CH_ACCESS_TOKEN)
	args = {'page':'1', 'per_page':'100'}
	rsp4 = api.execute_method('cooperhewitt.exhibitions.getList', args)

	return render_template('index.html',
							rsp4=rsp4)




@app.route("/<int:ex_id>")
def exhibitiion(ex_id):
	return build_page(ex_id)

def build_page(ex_id):
	api = cooperhewitt.api.multiclient.OAuth2(CH_ACCESS_TOKEN)

	reqs = (
		('cooperhewitt.exhibitions.getInfo', {'exhibition_id': ex_id}),
		('cooperhewitt.exhibitions.getObjects', {'on_display': '1', 'exhibition_id': ex_id, 'has_images': '1', 'page':'1', 'per_page':'100'}),	
		#('cooperhewitt.objects.tags.getTags', {'object_id': obj_id, 'page':'1', 'per_page':'100'}),
		#('cooperhewitt.objects.isOnDisplay', {'object_id': obj_id, 'page':'1', 'per_page':'100'}),
	)

	# 	retrieving exhibition info through another api	w/ exhibition id		
	rsp2 = api.execute_method(*reqs[0])
	print pprint.pformat(rsp2)
 

	# 	retrieving images for respective exhibition			
	rsp = api.execute_method(*reqs[1])
	print pprint.pformat(rsp)

	data = rsp['objects']
	for item in data:
		obj_id = item['id']

		reqs2 = (
			('cooperhewitt.objects.tags.getTags', {'object_id': obj_id, 'page':'1', 'per_page':'100'}),
			('cooperhewitt.objects.isOnDisplay', {'object_id': obj_id, 'page':'1', 'per_page':'100'}),	
		)
		
		tagsarray = api.execute_method(*reqs2[0])
		item['tags'] = tagsarray['tags']
		print pprint.pformat(tagsarray)

		locationarray = api.execute_method(*reqs2[1])
		item['locationinfo'] = locationarray
		print pprint.pformat(locationarray)
				
	return render_template('obj_page.html',
							data=data,
							rsp2=rsp2)
	

if __name__ == "__main__":
	app.run()
