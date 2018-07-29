
from lxml import html
from lxml import etree
import time
import requests
import sys

headers = {'user-agent' : 'Macintosh; Intel Mac OS X 10.11.6; Stephen TH Sher / stsher@iu.edu / Indiana University Informatics Researcher / IRB Study 1802176667'}

GDQ = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])

# fout = open("testing.txt", "a")
fout = open(GDQ + "_donations.txt", "a")


for pagenum in range(start, end + 1):

	url = "https://gamesdonequick.com/tracker/donations/" + GDQ[4:] + GDQ[:-4] + "?page=" + str(pagenum)

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
		name = html[pos1 + 6 : pos2 - 2]

		if name == "(Anonymous)":
			fout.write("Anonymous\n")
		else:
			fout.write(name[name.find(">",0) + 1 : name.find("<", 1)] + "\n")


		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		#time
		timestamp = html[pos1 + 6 : pos2 - 2]
		timestamp = timestamp[timestamp.find(">",0) + 1 : timestamp.find("<",1)]

		fout.write(timestamp + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		#donation

		donation = html[pos1 + 6 : pos2 - 2]
		# https://gamesdonequick.com/tracker/donation/437824
		donationURL = "https://gamesdonequick.com" + donation[donation.find("<a href=", 0) + 9 : donation.find(">",0) - 1]
		donationAmount = donation[donation.find(">",0) + 1 : donation.find("<",1)]

		fout.write(donationAmount + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		#comment
		comment = html[pos1 + 6 : pos2 - 2]

		if comment == "Yes":
			time.sleep(.5)

			print("Scraping", donationURL)

			commentPage = None
			commentHTML = None

			try:
				commentPage = requests.get(donationURL, headers=headers)
				commentHTML = str(commentPage.content)
			except:
				print("Timeout for 180 sec")
				time.sleep(180)
				commentPage = requests.get(donationURL, headers=headers)
				commentHTML = str(commentPage.content)

			if commentHTML.find("(Comment rejected") != -1:
				fout.write("Comment rejected\n")
			elif commentHTML.find("(Comment pending approval)") != -1:
				fout.write("Comment pending approval")
			elif commentHTML.find("<hr>", 0) == -1:
				fout.write("No comment\n")
			else:
				message = commentHTML[commentHTML.find("commentstate", 0) + 16 : commentHTML.find("<hr>", 0)]
				fout.write(message + "\n")

		else:
			fout.write("No comment\n")

		fout.write("\n")
		fout.flush()

		#move to next <td> instance
		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

	time.sleep(.5)

fout.close()
