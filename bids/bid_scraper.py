# from lxml import html
# from lxml import etree
import time
import requests
import sys

headers = {'user-agent' : 'Macintosh; Intel Mac OS X 10.11.6; Stephen TH Sher / stsher@iu.edu / Indiana University Informatics Researcher / IRB Study 1802176667'}

GDQs = ["2012agdq", "2012sgdq", "2013agdq", "2013sgdq", "2014agdq", "2014sgdq", "2015agdq", "2015sgdq", "2016agdq", "2016sdgq", "2017agdq", "2017sgdq", "2018agdq", "2018sgdq", "2019agdq"]

# GDQ = sys.argv[1]
# start = int(sys.argv[2])
# end = int(sys.argv[3])

def subTable(html, fout, pos, layer):
	if(layer == 1):
		fout.write("\n")

	# find </table
	table_end = html.find("</table>", pos[0])

	# Move beyond <td colspan
	pos[0] = html.find("<td", pos[0] + 3)


	while(pos[0] < table_end):

		# Option name
		option_raw = html[pos[0] : pos[1]]

		dump_n = option_raw.find("\\n",0)
		# dump_n = option_raw.find("\\n",dump_n)

		first_n = option_raw.find("\\n",dump_n + 1)
		second_n = option_raw.find("\\n", first_n + 1)

		option = option_raw[first_n + 2 : second_n]
		fout.write(str(layer) + " - Bid option\n")
		fout.write("Incentive: " + option + "\n")
		
		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Run name
		bid_run = html[pos[0] : pos[1]]

		first_n = bid_run.find("\\n",0)
		second_n = bid_run.find("\\n", first_n + 1)

		fout.write("Game: " + bid_run[first_n + 2 : second_n] + "\n")

		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Description
		bid_des = html[pos[0] : pos[1]]

		first_n = bid_des.find("\\n",0)
		second_n = bid_des.find("\\n", first_n + 1)

		fout.write("Description: " + bid_des[first_n + 2 : second_n] + "\n")

		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Dump
		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Amount
		bid_amount = html[pos[0] : pos[1]]

		first_n = bid_amount.find("\\n",0)
		second_n = bid_amount.find("\\n", first_n + 1)

		fout.write("Amount: " + bid_amount[first_n + 2 : second_n - 1] + "\n")

		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Goal
		bid_goal = html[pos[0] : pos[1]]

		first_n = bid_goal.find("\\n",0)
		second_n = bid_goal.find("\\n", first_n + 1)

		fout.write("Goal: " + bid_goal[first_n + 2 : second_n] + "\n")

		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		if(pos[0] == -1):
			break
		if(pos[0] < table_end):
			fout.write("\n")

		# next table start
		if(html.find("<table", pos[0]) != -1):
			table = html.find("<table ", pos[0])

			# subTable when </td> is past <table
			if (pos[1] > table):
			# if goal == "(None)":
				print("sub-sub-table")
				# pos[0] = html.find("<td", pos[0] + 3)
				subTable(html, fout, pos, layer + 1)

	# Move beyond </td>
	pos[1] = html.find("</td>", pos[1] + 1)





def scrape(GDQ):

	pos = [0,0]
	layer = 0

	# fout = open("testing.txt", "a")
	fout = open("plaintext/" + GDQ + "_incentives.txt", "w+")

	# url = "https://gamesdonequick.com/tracker/donations/" + GDQ[4:] + GDQ[:-4] + "?page=" + str(pagenum)
	# https://gamesdonequick.com/tracker/bids/agdq2012
	url = "https://gamesdonequick.com/tracker/bids/" + GDQ[4:] + GDQ[:-4]

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

	# fout.write(html)



	pos[0] = html.find("<td", 0)
	pos[1] = html.find("</td>", 0)


	while pos[0] != -1:

		# Incentive name name
		incentive_raw = html[pos[0] : pos[1]]

		# Clean up name
		a_start = incentive_raw.find("<a", 0)
		a_end = incentive_raw.find(">", a_start)
		incentive = incentive_raw[a_end :]

		incentive = incentive[3:incentive.find("a>", 0)-4]


		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Game name
		game_raw = html[pos[0] : pos[1]]

		first_n = game_raw.find("\\n",0)
		second_n = game_raw.find("\\n", first_n + 1)

		game = game_raw[first_n + 2:second_n]

		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Dump
		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Description
		des_raw = html[pos[0] : pos[1]]

		first_n = des_raw.find("\\n",0)
		second_n = des_raw.find("\\n", first_n + 1)

		des = des_raw[first_n + 2:second_n]

		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Amount
		amount_raw = html[pos[0] : pos[1]]

		first_n = amount_raw.find("\\n",0)
		second_n = amount_raw.find("\\n", first_n + 1)

		amount = amount_raw[first_n + 2:second_n]
		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Goal
		goal_raw = html[pos[0] : pos[1]]

		first_n = goal_raw.find("\\n",0)
		second_n = goal_raw.find("\\n", first_n + 1)

		goal = goal_raw[first_n + 2:second_n]
		pos[0] = html.find("<td", pos[0] + 1)
		pos[1] = html.find("</td>", pos[1] + 1)

		# Write
		if(goal == "(None)"):
			fout.write(str(layer) + " - Bid War\n")
		else:
			fout.write(str(layer) + " - Donation Goal\n")
		fout.write("Incentive: " + incentive + "\n")
		fout.write("Game: " + game + "\n")
		fout.write("Description: " + des + "\n")
		fout.write("Amount: " + amount + "\n")
		fout.write("Goal: " + goal + "\n")


		# next table start
		if(html.find("<table", pos[0]) != -1):
			table = html.find("<table ", pos[0])

			# subTable when </td> is past <table
			if (pos[1] > table):
			# if goal == "(None)":		
				subTable(html, fout, pos, layer + 1)

		fout.write("\n")

	fout.close()

def main():
	for GDQ in GDQs:
		scrape(GDQ)
		time.sleep(1)

main()


