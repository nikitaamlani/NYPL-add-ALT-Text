#!/usr/bin/python

import json
import os.path
import re
import requests
import string
import sys
import urllib

api_base = 'http://api.repo.nypl.org/api/v1/'
img_url_base = "http://images.nypl.org/index.php?id="
url_for_FSA = 'http://api.repo.nypl.org/api/v1/items/search?q=Farm%20Security%20Administration%20Photographs&field=topic&page={0}&per_page={1}'
token = 'gy5zj18sf99ddtxn'
deriv_type = 'r'.lower()


def main():
	current = 1
	total_pages = 1
	count = 50
	uuids = set()
	while current <= total_pages:
		url = url_for_FSA.format(current, count)
		current += 1
		response_for_FSA = requests.get(url, headers={'Authorization ':'Token token=' + token}).json()
		result_list = response_for_FSA['nyplAPI']['response']['result']
		total_pages = int(response_for_FSA['nyplAPI']['request']['totalPages'])
		for result in result_list:
			if result.get('typeOfResource') == 'still image':
				uuids.add(result['uuid'])
	id = 1
	for uuid in uuids:
		downloadImage(uuid, id)
		id += 1

def downloadImage(uuid, id):
	captures = []
	capture_response = getCaptures(uuid)
	item_response = getItem(uuid)
	container_response = getContainer(uuid)

	is_container = int(container_response['nyplAPI']['response']['numItems'])
	number_of_captures = int(capture_response['nyplAPI']['response']['numResults'])

	#######

	#Let's get started!

	#Make sure it's a valid UUID
	if re.search(r'([^a-f0-9-])', uuid) or len(uuid) != 36:
		sys.exit("That doesn't look like a correct UUID -- try again!")
	else:
		print("OK, that ID is well formed, looking it up now...")

	#Check to make sure we don't accidentally have a container or a collection UUID here
	if is_container > 0 and number_of_captures > 0:
		sys.exit("This is a container, this script is meant to pull images from single items only.")
	#If we're good to go, either get the number of capture IDs, or go to the item UUID and get the # of captures there
	else:
		print("Yep, this is a usable UUID, let's see what we can do with it...")
		if number_of_captures > 0: 
			print("%s captures total" % (number_of_captures))
			print(uuid)
		else:
			print("No captures in the API response! Trying to see if this is a capture UUID instead of an item UUID...")
			uuid = getItem(uuid)['nyplAPI']['response']['mods']['identifier'][-1]['$']
			item_response = getCaptures(uuid)
			capture_response = getCaptures(uuid)
			number_of_captures = int(item_response['nyplAPI']['response']['numResults'])
			print("Ah yes -- correct item UUID is " + uuid)
			print("Item UUID has %s capture(s) total" % (number_of_captures))

	#OK, enough checking, let's get the actual captures!
	for i in range(number_of_captures):
		capture_id = capture_response['nyplAPI']['response']['capture'][i]['imageID']
		captures.append(capture_id)

	#Grab the item title, and do some cleanup to make it usable as a folder name
	title = ("Trial_{0}").format(id)
	print("folder title will be '"+title+"'")

	#Create folder based on the item title
	if not os.path.exists(title):
		os.makedirs(title)
		
	if not os.path.isfile(title+'/'+'Readme.txt'):
		f = open(title+'/'+'Readme.txt', 'w')
		f.write(str(capture_response['nyplAPI']['response']['capture'][0]['title']))
		f.close()

	#Create the kind of deriv in the item-title folder
	for i in range(number_of_captures):
		if not os.path.isfile(title+'/'+str(captures[i])+deriv_type+'.jpg'):
			urllib.request.urlretrieve(img_url_base+str(captures[i])+'&t='+deriv_type,title+'/'+str(captures[i])+deriv_type+'.jpg')
			print(captures[i], deriv_type, i+1, "of", number_of_captures)
			i+=1
		else:
			print("file %s as %s deriv type already exists" % (captures[i], deriv_type))
			i+=1

#functions to get captures for a given UUID depending on whether it's a capture, item, or a container/collection
def getCaptures(uuid):
    url = api_base + 'items/' + uuid + '?withTitles=yes&per_page=100'
    call = requests.get(url, headers={'Authorization ':'Token token=' + token})
    return call.json()

def getItem(uuid):
	url = api_base + 'items/mods/' + uuid + '?per_page=100'
	call = requests.get(url, headers={'Authorization':'Token token=' + token}) 
	return call.json()

def getContainer(uuid):
	url = api_base + '/collections/' + uuid + '?per_page=100'
	call = requests.get(url, headers={'Authorization':'Token token=' + token}) 
	return call.json()
	
if __name__ == "__main__":
	main()