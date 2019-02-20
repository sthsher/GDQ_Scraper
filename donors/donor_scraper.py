
from lxml import html
from lxml import etree
import time
import requests
import sys

headers = {'user-agent' : 'Macintosh; Intel Mac OS X 10.11.6; Stephen TH Sher / stsher@iu.edu / Indiana University Informatics Researcher / IRB Study 1802176667'}

start = int(sys.argv[1])
end = int(sys.argv[2])

# fout = open("testing.txt", "a")
fout = open("donors.txt", "a")


for pagenum in range(start, end + 1):

	url = "https://gamesdonequick.com/tracker/donors/?page=" + str(pagenum)

	print("Scraping", url)

	page = None
	html = None

	try:
		page = requests.get(url, headers=headers)
		html = str(page.content)
	except:
		print("Timeout for 180 sec")
		time.sleep(180)
		page = requests.get(url, headers=headers)
		html = str(page.content)

	pos1 = html.find("<td>", 0)
	pos2 = html.find("</td>", 0)


	while pos1 != -1:
		#name
		name = html[pos1 + 6 :pos2]
		donorURL =  "https://gamesdonequick.com" + name[name.find("<a href=", 0) + 9 : name.find(">",0) - 1]
		name = html[pos1 + 6 : pos2 - 2]

		if name == "(Anonymous)":
			fout.write("Anonymous\n")
		else:
			fout.write(name[name.find(">",0) + 1 : name.find("<", 1)] + "\n")


		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		#total and count
		totalCount = html[pos1 + 6 : pos2 - 2]
		total = totalCount[totalCount.find(">",0) + 1 : totalCount.find("(",0) - 1]
		count = totalCount[totalCount.find("(",0) + 1: totalCount.find(")",0)]

		fout.write(total + "\n")
		fout.write(count + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		#max and avg donation

		maxAvg = html[pos1 + 6 : pos2 - 2]
		
		maxDonation = maxAvg[: maxAvg.find("/",0)]
		avgDonation = maxAvg[maxAvg.find("/",0) + 1:]

		fout.write(maxDonation + "\n")
		fout.write(avgDonation + "\n")
		fout.write(donorURL + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		fout.write("\n")
		fout.flush()

	time.sleep(.5)

fout.close()
