#!/usr/bin/env python

from sys import argv
import json
import cooperhewitt.api.client
import os
import urllib
import secrets

if __name__ == "__main__":
	
	api = cooperhewitt.api.client.OAuth2(secrets.ACCESS_TOKEN)

	args = {'exhibition_id': '68744915', 'has_images': '1', 'page':'1', 'per_page':'100'}

	rsp = api.execute_method('cooperhewitt.exhibitions.getObjects', args)

	target = open('book.md', 'w')

	for item in rsp['objects']:

		obj_id = item['id']
		
		images = item['images']
		if images:
			print obj_id
			print images[0]
			
			img = images[0]['n']['url']	
			target.write("![Object ID: "+obj_id+"]("+img+")")
		target.write("\n")			
														
		# First Section-includes: Title, Date
		title =	item['title'].encode('utf-8')
		target.write("# " + title)
		target.write("\n")
		
		if (item['date']):
			date = item['date'].encode('utf-8')
			target.write("## " + date)
		target.write("\n")

		target.write("___")	
		target.write("\n")

		# Second Section-includes: Designer, Manufacturer, Material, Donor Info.
		if (item['participants']):
			for item2 in item['participants']:
				role_name = item2['role_name'].encode('utf-8')
				if role_name == 'Designer':

					target.write("+ Designed by " + item2['person_name'].encode('utf-8'))
					target.write("\n")

		if (item['participants']):
			for item2 in item['participants']:
				role_name = item2['role_name'].encode('utf-8')
				if role_name == 'Manufacturer':

					target.write("+ Manufactured by " + item2['person_name'].encode('utf-8'))
					target.write("\n")

		if (item['medium']):
			medium = item['medium'].encode('utf-8')
			target.write("+ " + medium)
			target.write("\n")

		if (item['creditline']):
			creditline = item['creditline'].encode('utf-8')
			target.write("+ " + creditline)
		target.write("\n")		
		
		target.write("___")	
		target.write("\n")
		
		# retrieving tags through another api	
		obj_id = item['id']
		
		args = {'object_id': obj_id, 'page':'1', 'per_page':'100'}
		rsp2 = api.execute_method('cooperhewitt.objects.tags.getTags', args)
		# Third Section-includes: List of tags, Label Text
		
		first = True
		for tag in rsp2['tags']:
			tag_name = tag['name']
			if tag_name != None:
				
				if first:
					first = False
					target.write("+ ")
					target.write(tag_name)
				else:
					target.write(", " + tag_name)
		target.write("\n")

		if (item['label_text']):
			label_text = item['label_text'].encode('utf-8')
			target.write("+ " + label_text)
			target.write("\n")
		
		target.write("___")	
		target.write("\n")
		target.write("\n")
	
	target.close()