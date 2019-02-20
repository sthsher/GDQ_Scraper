import sys

GDQs = ["2012agdq", "2012sgdq", "2013agdq", "2013sgdq", "2014agdq", "2014sgdq", "2015agdq", "2015sgdq", "2016agdq", "2016sdgq", "2017agdq", "2017sgdq", "2018agdq", "2018sgdq", "2019agdq"]

def convert(GDQ):
	fout = open("csv/" + GDQ + "_incentives.csv", "w+")
	fout.write("\"Type\",\"Incentive\",\"Game\",\"Description\",\"Amount\",\"Goal\"\n")

	with open("plaintext/" + GDQ + "_incentives.txt") as fin:
		lines = fin.readlines()
		i = 0
		while (i < len(lines)):
			# Type
			fout.write("\"" + lines[i][:-1] + "\",")
			i += 1

			# Incentive
			fout.write("\"" + lines[i][11:-1] + "\",")
			i += 1

			# Game
			fout.write("\"" + lines[i][6:-1] + "\",")
			i += 1

			# Description
			fout.write("\"" + lines[i][13:-1] + "\",")
			i += 1

			# Amount
			fout.write("\"" + lines[i][8:-1] + "\",")
			i += 1

			# Goal
			fout.write("\"" + lines[i][6:-1] + "\"\n")
			i += 1

			# Dump
			i += 1

	fout.close()

def main():
	for GDQ in GDQs:
		convert(GDQ)

main()