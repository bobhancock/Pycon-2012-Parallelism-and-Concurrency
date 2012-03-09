#include <iostream>
#include <fstream>

using namespace std;

int main ()
{
  int c = 0;
  string line;
  ifstream bigfile("/home/rhancock/bigfile.xferlog");

  if(bigfile.is_open())
	{
	  while(! bigfile.eof()) 
		{
		  getline(bigfile,line);
		  //does it contain ssbrtg?
		  if(line.find("ssbrtg") != string::npos)
			c++;
		}
	  cout << c;
	  return 0;
	}
}
