#!/usr/bin/env python

from sys import argv
import json
import cooperhewitt.api.client
import os

ACCESS_TOKEN = os.getenv('CH_ACCESS_TOKEN')

if __name__ == "__main__":
	
	api = cooperhewitt.api.client.OAuth2(ACCESS_TOKEN)

	args = {'exhibition_id': '68744913', 'has_images': '1', 'page':'1', 'per_page':'100'}

	rsp = api.execute_method('cooperhewitt.exhibitions.getObjects', args)

	target = open('book.md', 'w')

	for item in rsp['objects']:
		
		title =	item['title'].encode('utf-8')
		target.write("# Title: " + title)
		target.write("\n")
		
		if (item['date']):
			date = item['date'].encode('utf-8')
			target.write("## Date: " + date)
			target.write("\n")
		
		if (item['medium']):
			medium = item['medium'].encode('utf-8')
			target.write("+ Medium: " + medium)
			target.write("\n")

		# retrieving tags through another api	
		obj_id = item['id']
		
		args = {'object_id': obj_id, 'page':'1', 'per_page':'100'}
		rsp2 = api.execute_method('cooperhewitt.objects.tags.getTags', args)

		target.write ("# ID: " + obj_id)
		target.write("\n")
		
		target.write("+ Tags: ")
		
		first = True
		
		for tag in rsp2['tags']:
			tag_name = tag['name']
			
			if first:
				first = False
				target.write(tag_name)
			else:
				target.write(", " + tag_name)

		target.write("\n")


		if (item['gallery_text']):
			gallery_text = item['gallery_text'].encode('utf-8')
			target.write("+ Info: " + gallery_text)
			target.write("\n")
		
		
		target.write("\n")
		target.write("\n")
	
	target.close()