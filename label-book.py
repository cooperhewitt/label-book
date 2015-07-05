#!/usr/bin/env python

from sys import argv
import json
import cooperhewitt.api.client
import os
import urllib


CH_ACCESS_TOKEN = os.environ['CH_ACCESS_TOKEN']

## adding flask here ( MJW/20150701 )
from flask import Flask, request
app = Flask(__name__)

#

@app.route("/")
def home():
	print request.url_root
	api = cooperhewitt.api.client.OAuth2(CH_ACCESS_TOKEN)

	args = {'page':'1', 'per_page':'100'}
	rsp4 = api.execute_method('cooperhewitt.exhibitions.getList', args)

	html = ""
	html += "<html>"
	html += "<head>"
	html += "<link rel=\"stylesheet\" type=\"text/css\" href=\"static/theme.css\">" 
	html += "</head>"
	html += "<body>"
	html += "<div class=\"object\">" 

	for ex_item in rsp4['exhibitions']:
		
		ex_list_id = ex_item['id']
		ex_list_title = ex_item['title']
				
		html += "<h1><a href = /" + request.url_root + ex_list_id + "\">" +  ex_list_title + "</h1>"

	html += "</div>" 
	html += "</body>"
	html += "</html>"
	
	return html


#

@app.route("/<int:ex_id>")
def exhibitiion(ex_id):
	return build_page(ex_id)

def build_page(ex_id):

	api = cooperhewitt.api.client.OAuth2(CH_ACCESS_TOKEN)

	args = {'exhibition_id': ex_id, 'has_images': '1', 'page':'1', 'per_page':'100'}
	rsp = api.execute_method('cooperhewitt.exhibitions.getObjects', args)

	html = ""
	html += "<html>"
	html += "<head>"
	html += "<link rel=\"stylesheet\" type=\"text/css\" href=\"static/theme.css\">" 
	html += "</head>"
	html += "<body>"


	# 	INTRO PAGE		
	# 	retrieving exhibition info through another api	w/ exhibition id		
	args = {'exhibition_id': ex_id}
	rsp3 = api.execute_method('cooperhewitt.exhibitions.getInfo', args)
	
	exhibition = rsp3['exhibition']
	extitle = exhibition['title'].encode('utf-8')
	extext = exhibition['text'].encode('utf-8')
	
	html += "<div class=\"object intro\">" 
	html += "<h1>" + extitle + "</h1>"
	html += "<p>" + extext + "</p>"			
	html += "</div>"
				
	# 	end INTRO PAGE

	for item in rsp['objects']:
		html += "<div class=\"object\">" 

		# store object ID in 'obj_id'		
		obj_id = item['id']

		# find images[]		
		images = item['images']

		# if statement to find index value of [0] in images[] and exclude images[] that are null		
		html += "<div class=\"col-1-3\">"
		if images:
			img = images[0]['n']['url']	
			img = "<img src=\"" + img + "\">"
			html += img.encode('utf-8')
		else: 
			html += "<h1>NO IMAGE</h1>"
		
		html += "</div>"

		html += "<div class=\"col-2-3\">"
		
		# sect. I														
		html += "<div class=\"section\">"
		
		# sect. I - title
		if item['title_raw']:
			title_raw =	item['title_raw'].encode('utf-8')
			# print obj_id
			# print title_raw
			html += "<h1>" + title_raw + "</h1>"
		else:	
			title =	item['title'].encode('utf-8')
			# print obj_id
			# print title	
			html += "<h1>" + title + "</h1>"

		# sect. I - date		
		if (item['date']):
			date = item['date'].encode('utf-8')
			html += "<h2>" + date + "</h2>"

		html += "</div>"
		# end sect. I														
		
		# sect. II
		html += "<div class=\"section\">"
		html += "<ul class=\"info\">"													

		# sect. II - particpants[] role_name: designer
		if (item['participants']):
			for item2 in item['participants']:
				role_name = item2['role_name'].encode('utf-8')
				if role_name == 'Designer':
					html += "<li>Designed by " + item2['person_name'].encode('utf-8') + "</li>"
					
		# sect. II - particpants[] role_name: manufacturer
		if (item['participants']):
			for item2 in item['participants']:
				role_name = item2['role_name'].encode('utf-8')
				if role_name == 'Manufacturer':
					html += "<li>Manufactured by " + item2['person_name'].encode('utf-8') + "</li>"				

		# sect. II - medium
		if (item['medium']):
			medium = item['medium'].encode('utf-8')
			html += "<li>" + medium + "</li>"

		# sect. II - creditline
		if (item['creditline']):
			creditline = item['creditline'].encode('utf-8')
			html += "<li>" + creditline + "</li>"
								
		html += "</ul>"
		html += "</div>"
		# end sect. II

		# sect. III
															
		# sect. III - tags		
		# retrieving tags through another api	w/ obj id		
		args = {'object_id': obj_id, 'page':'1', 'per_page':'100'}
		rsp2 = api.execute_method('cooperhewitt.objects.tags.getTags', args)
				
		tags = rsp2['tags']
		
		if tags:
			html += "<div class=\"section\">"
			html += "<ul class=\"tags\">"													
			
			for tag in rsp2['tags']:
				tag_name = tag['name']
				
				if tag_name != None:
					html += "<li>" + tag_name.encode('utf-8') + "</li>"
	
			html += "</ul>"
			html += "</div>"
				
			# end sect. III

			# sect. IV
													
		# sect. IV - label text
		if (item['label_text']) != None:
			html += "<div class=\"section\">"
			html += "<p>"
			
			label_text = item['label_text'].encode('utf-8')
			html += label_text + "</p>"

			html += "</div>"
		# end sect. IV

		html += "</div>" #col-2-3 div
		html += "</div>" #object div 	
	return html
	
if __name__ == "__main__":
	### note: this is setup for a local config. need to add proper settings for heroku ( MJW/20150701 )
    app.run()