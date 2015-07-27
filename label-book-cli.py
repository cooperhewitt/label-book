#!/usr/bin/env python

from sys import argv
import os

import argparse

import json
import yaml

import cooperhewitt.api.client


CH_ACCESS_TOKEN = os.environ['CH_ACCESS_TOKEN']


def get_object_data(obj_id):
	api = cooperhewitt.api.client.OAuth2(CH_ACCESS_TOKEN)

	args = {'id': obj_id}
	rsp = api.execute_method('cooperhewitt.objects.getInfo', args)

	data = rsp['object']
	
	out = {}
	
# 	title
	if data['title_raw']:
		out['title'] = data['title_raw']
	else:
		out['title'] = data['title']

# 	date
	if data['date']:
		out['date'] = data['date']

# 	image
	if data['images']:
		out['image'] = data['images'][0]['z']['url']
	else:
		out['image'] = "No Image"

# 	participants		
	if data['participants']:
		for item2 in data['participants']:
			if item2['role_name'] == 'Designer':
				out['designer'] = item2['person_name']
			if item2['role_name'] == 'Manufacturer':
				out['manufacturer'] = item2['person_name']

# 	medium		
	if data['medium']:
		out['medium'] = data['medium']
		
# 	creditline
	if data['creditline']:
		out['creditline'] = data['creditline']

# 	label_text
	if data['label_text']:
		out['label_text'] = data['label_text']

# 	MISSING TAGS
# 	MISSING LOCATION INFO
			
	return out

def harvest_exhbition_data(ex_id):
	api = cooperhewitt.api.client.OAuth2(CH_ACCESS_TOKEN)

	args = {'exhibition_id': ex_id}
	rsp2 = api.execute_method('cooperhewitt.exhibitions.getInfo', args)

	args = {'on_display': '1', 'exhibition_id': ex_id, 'has_images': '1', 'page':'1', 'per_page':'100'}
	rsp = api.execute_method('cooperhewitt.exhibitions.getObjects', args)

	data = rsp['objects']

	for item in data:
		
		obj_id = item['id']

		args = {'object_id': obj_id, 'page':'1', 'per_page':'100'}
		tags = api.execute_method('cooperhewitt.objects.tags.getTags', args)
		locations = api.execute_method('cooperhewitt.objects.isOnDisplay', args)

		item['tags'] = tags['tags']		
		item['locationinfo'] = locations

		return data
	

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Build the exhibiton books.')

	parser.add_argument('-e', '--exhibition', dest='exhibition', action='store', help='An exhbition id.')
	parser.add_argument('-o', '--object', dest='object', action='store', help='An object id.')
	args = parser.parse_args()

	if (args.object):
		output = get_object_data(args.object)

	yml = yaml.safe_dump(output, default_flow_style=False, explicit_start=True)
	print yml

	target = open('2015-07-22.md', 'w+')
	target.write(yml)