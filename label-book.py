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

	target = open('book.html', 'w')

	target.write("<html>") 
	target.write("<head>")
	target.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"theme.css\">")  
	target.write("</head>") 
	target.write("<body>")


# 	INTRO PAGE		
# 	retrieving exhibition info through another api	w/ exhibition id		
	args = {'exhibition_id': '68744915'}
	rsp3 = api.execute_method('cooperhewitt.exhibitions.getInfo', args)
	
	exhibition = rsp3['exhibition']
	extitle = exhibition['title'].encode('utf-8')
	extext = exhibition['text'].encode('utf-8')
	
	target.write("<div class=\"object intro\">") 
	target.write("<h1>" + extitle + "</h1>")
	target.write("<p>" + extext + "</p>")			
	target.write("</div>")
				
# 	end INTRO PAGE



	for item in rsp['objects']:
		target.write("<div class=\"object\">") 

# 		store object ID in 'obj_id'		
		obj_id = item['id']



# 		find images[]		
		images = item['images']

# 		if statement to find index value of [0] in images[] and exclude images[] that are null		
		target.write("<div class=\"col-1-3\">")
		if images:
			img = images[0]['n']['url']	
			target.write("<img src=\"" + img + "\">")
		else: 
			target.write("<h1>NO IMAGE</h1>")
		target.write("</div>")


		target.write("<div class=\"col-2-3\">")
# 		sect. I														
		target.write("<div class=\"section\">")
		
# 		sect. I - title
		if item['title_raw']:
			title_raw =	item['title_raw'].encode('utf-8')
# 			print obj_id
# 			print title_raw
			target.write("<h1>" + title_raw + "</h1>")
		else:	
			title =	item['title'].encode('utf-8')
# 			print obj_id
# 			print title	
			target.write("<h1>" + title + "</h1>")

# 		sect. I - date		
		if (item['date']):
			date = item['date'].encode('utf-8')
			target.write("<h2>" + date + "</h2>")

		target.write("</div>")
# 		end sect. I														
	
	
	
	
			

# 		sect. II
		target.write("<div class=\"section\">")
		target.write("<ul class=\"info\">")													

# 		sect. II - particpants[] role_name: designer
		if (item['participants']):
			for item2 in item['participants']:
				role_name = item2['role_name'].encode('utf-8')
				if role_name == 'Designer':
					target.write("<li>Designed by " + item2['person_name'].encode('utf-8') + "</li>")
					
# 		sect. II - particpants[] role_name: manufacturer
		if (item['participants']):
			for item2 in item['participants']:
				role_name = item2['role_name'].encode('utf-8')
				if role_name == 'Manufacturer':
					target.write("<li>Manufactured by " + item2['person_name'].encode('utf-8') + "</li>")				

# 		sect. II - medium
		if (item['medium']):
			medium = item['medium'].encode('utf-8')
			target.write("<li>" + medium + "</li>")

# 		sect. II - creditline
		if (item['creditline']):
			creditline = item['creditline'].encode('utf-8')
			target.write("<li>" + creditline + "</li>")
								
		target.write("</ul>")
		target.write("</div>")
# 		end sect. II



# 		sect. III
															
# 		sect. III - tags		
# 		retrieving tags through another api	w/ obj id		
		args = {'object_id': obj_id, 'page':'1', 'per_page':'100'}
		rsp2 = api.execute_method('cooperhewitt.objects.tags.getTags', args)
				
		tags = rsp2['tags']
		
		if tags:
			target.write("<div class=\"section\">")
			target.write("<ul class=\"tags\">")													
			
			for tag in rsp2['tags']:
				tag_name = tag['name']
				
				if tag_name != None:
					target.write("<li>" + tag_name + "</li>")
	
			target.write("</ul>")
			target.write("</div>")
				
# 		end sect. III



# 		sect. IV
													
# 		sect. IV - label text
		if (item['label_text']) != None:
			target.write("<div class=\"section\">")
			target.write("<p>")
			
			label_text = item['label_text'].encode('utf-8')
			target.write(label_text + "</p>")

			target.write("</div>")
# 		end sect. IV

		target.write("</div>") #col-2-3 div
		target.write("</div>") #object div 	
	target.close()