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

    // Tabu Search with 100000 evaluations
    TabuSearch ts(input);

    vector<int> solution =  ts.getSolution();
    cout << "Tabu Search: " << endl;
    cout << "\tCostA: " << ts.getCost() << endl;
    cout << "\tSolution: ";
    for (int i = 0; i < solution.size(); ++i)
        cout << solution[i] << " ";
    cout << endl;

    return 0;
}