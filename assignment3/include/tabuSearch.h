#ifndef TABUSEARCH_H__
#define TABUSEARCH_H__

#include "input.h"
#include "common.h"
#include <deque>
#include <queue>

using namespace std;
using namespace std::chrono;

typedef struct
{
    int i, j, posI, posJ;
} TabuMove;

typedef struct Neighbour
{
    int r, s, cost;
    bool operator<(const Neighbour &n) const
    {
        return cost < n.cost;
    }
    bool operator>(const Neighbour &n) const
    {
        return cost > n.cost;
    }
    bool operator==(const Neighbour &n) const
    {
        return cost == n.cost;
    }
} Neighbour;

class TabuSearch
{
public:
    explicit TabuSearch(const Input &input, int neighbourhoodSize = 10000, int maxFails = 2500);

    void execute();

    // Factorization
    int moveCost(vector<int> &oldSolution, int r, int s);
    // Calculate cost using objetive function
    int calculateCost(vector<int> &solution);

    // Tabu Search functions
    bool checkMove(int r, int s, vector<int> &currentSolution);

    void printSolution();

private:
    // Input data
    int dimension_;
    map< int, vector<int> > adjacency_;
    vector< vector<int> > distances_;
    vector< vector<int> > flow_;
    vector< int > frequencies_;

    // Tabu Moves
    deque<TabuMove> tabuList_;

    // Parameters
    int neighbourhoodSize_;
    int maxFails_;

    // Solution data
    vector<int> solution_;
    int cost_;
    double time_;
};

#endif