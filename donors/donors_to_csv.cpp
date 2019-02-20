//g++-4.8 -std=c++11

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc, char** argv)
{

	ifstream fin("donors.txt");
	ofstream fout("CSV/donors.csv");

	fout << "Name,Total Donation,Donation Count,Max Donation,Average Donation,Donor URL" << endl;

	while (!fin.eof())
	{
		string name;
		getline(fin, name);

		string total;
		getline(fin, total);

		string count;
		getline(fin, count);

		string maximum;
		getline(fin, maximum);

		string average;
		getline(fin, average);

		string url;
		getline(fin,url);

		string buffer;
		getline(fin, buffer);

		fout << "\"" << name << "\"" << "," << "\"" << total << "\"" << "," << count << "," << "\"" << maximum << "\"" << "," << "\"" << average << "\"" << "," << url << endl;

	}

	fin.close();
	fout.close();

	return 0;
}