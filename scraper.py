# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5033_BLBC_gov"
url = "http://brent.gov.uk/your-council/transparency-in-brent/open-data/monthly-spend/"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
blocks = soup.findAll('h2', {'class':'removeLowerMargin'})

for block in blocks:

	link = block.a['href']

	# add the right prefix onto the url
	pageUrl = link.replace("/your-council","http://www.brent.gov.uk/your-council")
	
	html2 = urllib2.urlopen(pageUrl)
	soup2 = BeautifulSoup(html2)
	
	csvYr = soup2.find('h1').contents[0]
	fileBlocks = soup2.findAll('li')
	
	for fileBlock in fileBlocks:
		print fileBlock
		fileUrl = fileBlock.a['href']
		fileUrl = fileUrl.replace("/your-council","http://www.brent.gov.uk/your-council")
		
		title = fileBlock.a.contents[0]
		
		if titleTest == None:
			print 'not a csv'
		else:
			# create the right strings for the new filename
			title = title.upper().strip()
			
			csvMth = title.split(' ')[0][:3]
			csvMth = convert_mth_strings(csvMth);
		
			filename = entity_id + "_" + csvYr + "_" + csvMth
		
			todays_date = str(datetime.now())
		
			scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date })
			
			print filename
