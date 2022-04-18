
#include <fstream>
#include <iostream>

using namespace std;

int main()
{
  ifstream data_r("soln");
  ofstream data_w("soln_fix");

  int a;
  while(data_r >> a)
  {
    if (a < 419)
      data_w << 0 << " ";
    else if (a < 419+47)
      data_w << 1 << " ";
    else if (a < 419+47+98)
      data_w << 2 << " ";
    else if (a < 419+47+98+79)
      data_w << 3 << " ";
    else if (a < 419+47+98+79+329)
      data_w << 4 << " ";
    else
      data_w << 5 << " ";
    /*
    if (a < 6)
      data_w << 0 << " ";
    else if (a < 19)
      data_w << 1 << " ";
    else if (a < 68)
      data_w << 2 << " ";
    else
      data_w << 3 << " ";*/
  }
  return 0;
}