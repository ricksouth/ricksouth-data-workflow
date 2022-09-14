# -*- coding: utf-8 -*-
#!/usr/bin/env python
from bs4 															import BeautifulSoup
import json
import requests
import patreon
import re
import os

sep = os.path.sep

def main():
	print("Starting to receive Github Sponsors, Ko-Fi Members and Patreons.\n")

	setVariables()

	kofimembers = []
	githubsponsors = []
	patrons = []

	githubresult = queryGithub()
	if 'data' in githubresult:
		ghdata = githubresult['data']
		if 'user' in ghdata:
			ghuser = ghdata['user']
			if 'sponsors' in ghuser:
				ghsponsors = ghuser['sponsors']
				if 'nodes' in ghsponsors:
					ghnodes = ghsponsors['nodes']
					for ghnode in ghnodes:
						if 'login' in ghnode:
							ghlogin = ghnode['login']
							githubsponsors.append(ghlogin)

	kofiresult = queryKoFi()
	for kresult in kofiresult:
		kofimembers.append(kresult.strip())

	print("Starting to get the list of Patreon patrons.")
	patreonresult = queryPatreon()
	for presult in patreonresult:
		patrons.append(presult.strip())

	githubsponsors = naturalsort(githubsponsors)
	kofimembers = naturalsort(kofimembers)
	patrons = naturalsort(patrons)

	print("Github sponsors: " + ", ".join(githubsponsors))
	print("Ko-Fi members: " + ", ".join(kofimembers))
	print("Patrons: " + ", ".join(patrons))

	dataout = {}
	dataout["github"] = githubsponsors
	dataout["kofi"] = kofimembers
	dataout["patreon"] = patrons
	dataout["combined"] = naturalsort(githubsponsors + kofimembers + patrons)

	with open("." + sep + "membership" + sep + "members.json", "w") as memberfile:
		memberfile.write(json.dumps(dataout, indent=4))

	return

def queryGithub():
	githubheaders = {"Authorization": "Bearer " + os.environ['GH_API']}
	githubquery = """{
					   user(login: "ricksouth") {
						 ... on Sponsorable {
						   sponsors(first: 100) {
							 totalCount
							 nodes {
							   ... on User {
								 login
							   }
							   ... on Organization {
								 login
							   }
							 }
						  }
						 }
					   }
					 }
				  """

	request = requests.post('https://api.github.com/graphql', json={'query': githubquery}, headers=githubheaders)
	if request.status_code == 200:
		return request.json()

	return {}

def queryKoFi():
	members = []

	html = requests.get(os.environ['SHEETS_URL']).text
	soup = BeautifulSoup(html, "lxml")

	tables = soup.find_all("table")
	index = 0
	for table in tables:
		rows = [[td.text for td in row.find_all("td")] for row in table.find_all("tr")]
		for row in rows:
			if len(row) < 1:
				continue
			if row[0] == "Ko-Fi Members":
				continue
			if row[0] == "":
				break

			members.append(row[0])
		break

	return members

def queryPatreon():
	api_client = patreon.API(os.environ['PATREON_API'])
	campaign_id = api_client.fetch_campaign().data()[0].id()
	cursor = None
	names = []
	while True:
		pledges_response = api_client.fetch_page_of_pledges(
			campaign_id,
			25,
			cursor=cursor,
		)
		getPatreonNames(pledges_response.data(), pledges_response, names)
		cursor = api_client.extract_cursor(pledges_response)
		if not cursor:
			break

	return names

def getPatreonNames(all_pledges, pledges_response, names):
	for pledge in all_pledges:
		patron_id = pledge.relationship('patron').id()
		patron = pledges_response.find_resource_by_type_and_id('user', patron_id)
		names.append(patron.attribute('full_name'))
		
	return

def naturalsort(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

def setVariables():
	return

if __name__ == "__main__":
	main()