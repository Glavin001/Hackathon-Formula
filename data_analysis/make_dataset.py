import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
from time import sleep
import csv,re
import traceback
import string
import os.path,sys
import cPickle as pickle

n,i,c=1,0,1
fields = ["winner","name","tagline","description","platforms","software","members","popularity"]

def replacePunctuation(line):
	line = line.decode("ascii")
	for ch in line:
		if ch in "~@#$%^&*()_-+=~<>?/,.;:!{}[]|'\"":
			line = line.replace(ch, " ")
	return line

hacks = []

b = open('data.csv', 'w')
csv_writer = csv.writer(b, quoting=csv.QUOTE_ALL)
csv_writer.writerow(fields)
while(True):
	i+=1
	print 'http://challengepost.com/software/trending?page='+str(i)
	response = urllib2.urlopen('http://challengepost.com/software/trending?page='+str(i))
	html = response.read() # raw html
	response.close()

	soup=BeautifulSoup(html) # beautify it
	# For each hack in page, analyze >>
	for a in soup.findAll('a'):
		link = ""
		try:
			link = a["href"]

			# Filter links that aren't hacks
			if link.startswith("/software/") and link!="/software/add?ref_feature=built-with&ref_medium=button" and "trending?page=" not in link:
				c+=1
				print "Total",c
				link = "http://challengepost.com"+link

				response_page = urllib2.urlopen(link)
				html_page = response_page.read()
				response_page.close()  # best practice to close the file
				soup_page=BeautifulSoup(html_page) 

				winner = ("winner label radius" in str(html_page))
				print winner
				tagline = ""
				#tagline = replacePunctuation(soup_page.find(id="app-tagline").text.replace("\n"," ").lower().strip())
				#if not tagline:
			#		raise ValueError("no tagline")		
				description = replacePunctuation(soup_page.find(id="app-details-left").text.replace("\n"," ").lower().strip())

				if not description:
					raise ValueError("no descipriotn")				
				platforms = [x.text for x in soup_page.findAll(**{"class":"label"})]
				if not platforms:
					raise ValueError("no platforms")				

				software = [x.text for x in soup_page.findAll(**{"class":"software-tag label recognized-tag"})]
				if not software:
					raise ValueError("no software")		


				name = soup_page.find(id="app-title").text.strip().lower()
				print name,link

				popularity = re.sub('[^0-9]','', soup_page.find(**{"class":"like-counts"}).text)
				if not popularity:
					popularity=0
				else:
					popularity=int(popularity)

				members = html_page.count("follow-text")
				hack = [winner,name,tagline,description,str(platforms),str(software),int(members),popularity]
				csv_writer.writerow(hack)
				hacks.append(hack)
				if os.path.isfile("SAVE_HACKS"):
					fff = open( "raw_data.p", "wb" )
					pickle.dump( hacks, fff )
					fff.close()

				print "wrote",n,i
				n+=1
			else:
				continue
		except Exception as e:
			# ??? -> Skip!, and go on
			print "error",e,link
			print sys.exc_traceback.tb_lineno 
			print 
			continue

	# do something

b.close()

