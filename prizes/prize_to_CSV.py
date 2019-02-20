import sys

GDQs = ["2013agdq", "2013sgdq", "2014agdq", "2014sgdq", "2015agdq", "2015sgdq", "2016agdq", "2016sdgq", "2017agdq", "2017sgdq", "2018agdq", "2018sgdq", "2019agdq"]

def convert(GDQ):
	fout = open("CSV/" + GDQ + "_prizes.csv", "w+")
	fout.write("\"Prize Name\",\"Contributor\",\"Minimum Bid\",\"Game Span\",\"Category\",\"Image\",\"Winner\",\"Winner URL\"\n")

	with open("plaintext/" + GDQ + "_prizes.txt") as fin:
		lines = fin.readlines()
		i = 0
		while (i < len(lines)):
			# Prize Name
			fout.write("\"" + lines[i][7:-1] + "\",")
			i += 1

			# Contributor
			fout.write("\"" + lines[i][13:-1] + "\",")
			i += 1

			# Bid
			fout.write("\"" + lines[i][5:-1] + "\",")
			i += 1

			# Game
			fout.write("\"" + lines[i][6:-1] + "\",")
			i += 1

			# Category
			fout.write("\"" + lines[i][10:-1] + "\",")
			i += 1

			# Image
			fout.write("\"" + lines[i][7:-1] + "\",")
			i += 1

			# Winner
			fout.write("\"" + lines[i][8:-1] + "\",")
			i += 1

			# Winner URL
			fout.write("\"" + lines[i][12:-1] + "\"\n")
			i += 1

	fout.close()

def main():
	for GDQ in GDQs:
		convert(GDQ)

main()