#include "common.h"
#include "input.h"
#include "tabuSearch.h"

using namespace std;

int main (int argc, char *argv[])
{

    if (argc < 2 || argc > 3)
    {
        cerr << "ERROR: Execute with: qap [data]" << endl;
        return -1;
    }

    // Read file
    Input input(argv[1]);
    if (!input.read())
    {
        cerr << "ERROR: Not file found";
        return -1;
    }

    // Tabu Search - neighbourhoodSize : 10000 - maxFails : 2500
    TabuSearch ts(input, 10000, 2500);

    return 0;
}