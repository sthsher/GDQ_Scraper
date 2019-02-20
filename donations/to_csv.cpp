//g++-4.8 -std=c++11

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc, char** argv)
{
	string GDQ = argv[1];

	ifstream fin(GDQ + "_donations.txt");
	ofstream fout("CSV/" + GDQ + "_donations.csv");

	fout << "Name,Date,Amount,Comment" << endl;

	while (!fin.eof())
	{
		string name;
		getline(fin, name);

		string time;
		getline(fin, time);

		time = time.substr(0, time.length() - 6);

		string amount;
		getline(fin, amount);

		string comment;
		getline(fin, comment);

		string buffer;
		getline(fin, buffer);

		// fout << "\"" << name << "\"" << "," << time << "," << amount << "," << "\"" << comment << "\"" << endl;		
		fout << "\"" << name << "\"" << "," << time << "," << "\"" << amount << "\"" << "," << "\"" << comment << "\"" << endl;		

	}

	fin.close();
	fout.close();

	return 0;
}