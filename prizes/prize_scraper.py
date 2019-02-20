import time
import requests
import sys

headers = {'user-agent' : 'Macintosh; Intel Mac OS X 10.11.6; Stephen TH Sher / stsher@iu.edu / Indiana University Informatics Researcher / IRB Study 1802176667'}

GDQs = ["2013agdq", "2013sgdq", "2014agdq", "2014sgdq", "2015agdq", "2015sgdq", "2016agdq", "2016sdgq", "2017agdq", "2017sgdq", "2018agdq", "2018sgdq", "2019agdq"]
# GDQs = ["2013agdq"]


page = None
html = None

for GDQ in GDQs:

	url = "https://gamesdonequick.com/tracker/prizes/" + GDQ[4:] + GDQ[:-4]
	fout = open("plaintext/" + GDQ + "_prizes.txt", "w+")
	print("Scraping", url)

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

		# Prize Name
		name_raw = html[pos1:pos2]

		# Dump one \n
		beg = html.find("\\n", pos1)
		beg = html.find("\\n", beg + 1)
		end = html.find("\\n", beg + 1)
		name = html[beg + 2 : end]

		fout.write("Prize: " + name + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		# Contributor
		contributor_raw = html[pos1:pos2]

		# One \n means no contributor
		beg = contributor_raw.find("\\n", 0)
		end = contributor_raw.find("\\n", beg + 1)

		contributor = ""

		if (end != -1):
			contributor = contributor_raw[beg + 2 : end]
		else:
			contributor = "Anonymous"

		fout.write("Contributor: " + contributor + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		# Minimum Bid
		bid_raw = html[pos1:pos2]

		beg = bid_raw.find("\\n", 0)
		end = bid_raw.find("\\n", beg + 1)

		fout.write("Bid: " + bid_raw[beg + 2 : end] + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		# Game Name
		game_raw = html[pos1:pos2]

		arrow = game_raw.find("fa fa-arrows-h", 0)
		game = ""

		if (pos2 - pos1 == 6):
			game = "None"
		elif (arrow == -1):
			# One game
			# Dump one \n
			beg = game_raw.find("\\n", 0)
			beg = game_raw.find("\\n", beg + 1)
			end = game_raw.find("\\n", beg + 1)
			game = game_raw[beg + 2 : end]
		else:
			# Span
			# First game
			# Dump 1 \n
			beg = game_raw.find("\\n", 0)
			beg = game_raw.find("\\n", beg + 1)
			end = game_raw.find("\\n", beg + 1)
			game1 = game_raw[beg + 2 : end]

			# Dump 2 \n
			beg = game_raw.find("\\n", beg + 1)
			beg = game_raw.find("\\n", beg + 1)
			beg = game_raw.find("\\n", beg + 1)
			beg = game_raw.find("\\n", beg + 1)
			end = game_raw.find("\\n", beg + 1)
			game2 = game_raw[beg + 2 : end]

			game = game1 + " -> " + game2


		fout.write("Game: " + game + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		# Category
		category_raw = html[pos1:pos2]

		beg = category_raw.find("\\n", 0)
		end = category_raw.find("\\n", beg + 1)

		fout.write("Category: " + category_raw[beg + 2 : end] + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		# Image
		image_raw = html[pos1:pos2]

		image_flag = image_raw.find("None", 0)

		image = ""

		if (image_flag == -1):
			# There is an image link
			beg = image_raw.find("\"", 0)
			end = image_raw.find("\"", beg + 1)
			image = image_raw[beg + 1 : end]
		else:
			image = "None"

		fout.write("Image: " + image + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

		# Winner
		winner_raw = html[pos1:pos2]

		winner_flag = winner_raw.find("Anonymous", 0)

		winner_url = ""
		winner = ""

		if (winner_flag != -1):
			winner = "Anonymous"
			winner_url = "Anonymous"
		else:
			url_beg = winner_raw.find("\"", 0)
			url_end = winner_raw.find("\"", url_beg + 1)

			winner_url = "https://gamesdonequick.com/" + winner_raw[url_beg + 1 : url_end]

			beg = url_end + 2
			end = winner_raw.find("</a>", 0)

			winner = winner_raw[beg : end]

		fout.write("Winner: " + winner + "\n")
		fout.write("Winner URL: " + winner_url + "\n")

		pos1 = html.find("<td>", pos1 + 1)
		pos2 = html.find("</td>", pos2 + 1)

	time.sleep(1)



fout.close()
