#include "tabuSearch.h"
#include <algorithm>
#include <random>
#include <cmath>
#include <fstream>

TabuSearch::TabuSearch(const Input &input, double neighbourhoodSize, int maxEvaluations, int maxFails)
    : dimension_(input.getDimension()), distances_(input.getDistances()), flow_(input.getFlow()), adjacencies_(input.getAdjacencies())
{
    solution_.resize(dimension_);

    // Fix parameters
    neighbourhoodSize_ = neighbourhoodSize;
    maxEvaluations_ = maxEvaluations;
    maxFails_ = maxFails;

    //Initialize frecuency matrix
    frec_.resize(dimension_);
    for (int i = 0; i < frec_.size(); ++i)
    {
        frec_[i].resize(dimension_);
    }
    execute();

}

void TabuSearch::execute()
{

    // Randdom
    std::default_random_engine gen;
    std::uniform_int_distribution<> dist_int(0, dimension_-1);
    std::uniform_real_distribution<double> dist_real(0.0,1.0);

    // Inner parameters
    int tabuLength = dimension_ / 10;
    int fails = 0;
    bool improvement = false;
    
    // Initialize
    for (int i = 0; i < dimension_; ++i)
        solution_[i] = i;

    // Shuffle vector
    std::shuffle(solution_.begin(), solution_.end(), gen);

    // Get cost
    cost_ = calculateCost(solution_);

    // Current solution and cost
    vector<int>currentSolution;
    currentSolution = solution_;
    int currentCost = cost_;

    double T = 100;

    cout << " Tabu search " << endl;
    bool isTabu = true;
    ofstream data_w("soln");
    while(true)
    {
        if (isTabu)
        {
        improvement = false;
        /*
        */

        
        // Empty the neighborhoud
        priority_queue<Neighbour, vector<Neighbour>, greater<Neighbour>> neighbourhood;

        // Generate the Neighbourhood
 	    //for(int r = 0; r < dimension_-1; r++)
      //{
        //for(int s = r+1; s < dimension_; s++)
        for (int i = 0; i < 10000; ++i)
        {
            // Generate random r and s
            //int r = rand() % dimension_;
            //int s = rand() % dimension_;
            int r = dist_int(gen);
            int s = dist_int(gen);

            // Add to the neighbourhood
            Neighbour neighbour;
            neighbour.r = r;
            neighbour.s = s;
            neighbour.cost = currentCost + moveCost(currentSolution, r, s);

            neighbourhood.push(neighbour);
        }
      //}


        // Check if the move is not Tabu
        bool selected = false;
        Neighbour best_neigh = neighbourhood.top();
        selected = checkMove(best_neigh.r, best_neigh.s, currentSolution);

        // Check if is better than our solution
        if (!selected && best_neigh.cost < cost_)
        {
            selected = true;
        }
        
        neighbourhood.pop();
        while (!selected &&  !neighbourhood.empty())
        {
            best_neigh = neighbourhood.top();
            if (best_neigh.cost != currentCost)
                selected = checkMove(best_neigh.r, best_neigh.s, currentSolution);
            neighbourhood.pop();
        }

        // If none of the neighbourhood is selected, generate new neighbourhood
        if (!selected)
            continue;
      

        int r =  best_neigh.r;
        int s =  best_neigh.s;

        // Jump to something
        std::swap(currentSolution[r], currentSolution[s]);
        currentCost = best_neigh.cost;
        
        if (currentCost < cost_)
        {
            improvement = true;
            solution_ = currentSolution;
            cost_ = currentCost;
            cout << "\tCost: " << cost_ << endl;
        }

        // Create tabu move
        TabuMove tabuMove;
        tabuMove.posI = currentSolution[r];
        tabuMove.posJ = currentSolution[s];
        tabuMove.i = r;
        tabuMove.j = s;

        // Add tabu move
        tabuList_.push_back(tabuMove);

        //Size of the deque
        if (tabuList_.size() > tabuLength)
        {
            tabuList_.pop_front();
        }

        if (improvement)
        {
            fails = 0;
        }
        else
        {
            fails ++;
            if (fails == 2500)
            {
                isTabu = false;
                cout << " Simulated annealing " << endl;
                currentSolution = solution_;
                currentCost = cost_;
            }
        }
    }
    else
    {
        int r = dist_int(gen);
        int s = dist_int(gen);

        double p = dist_real(gen);

        currentCost = cost_ + moveCost(currentSolution, r, s);

        if (currentCost < cost_)
        {
            std::swap(currentSolution[r], currentSolution[s]);
            solution_ = currentSolution;
            cost_ = currentCost;
            cout << "\tCost: " << cost_ << endl;
            /*
            if (cost_ == 311241)
            {
            for (int i = 0; i < solution_.size(); ++i)
            {
                data_w << solution_[i] << " ";
                cout << solution_[i] << " ";
            }
            data_w.close();
            cout << "End of the line" << endl;
            }*/
        }

        T *= 0.95;
    }
    }
}

int TabuSearch::moveCost(vector<int> &oldSolution, int r, int s)
{
    int cost = 0;
    for (int k : adjacencies_[r])
        if (k != s)
            cost += flow_[oldSolution[s]][oldSolution[k]] - flow_[oldSolution[r]][oldSolution[k]];
    
    for (int k : adjacencies_[s])
        if (k != r)
            cost += flow_[oldSolution[r]][oldSolution[k]] - flow_[oldSolution[s]][oldSolution[k]];

    return cost;
}

int TabuSearch::calculateCost(vector<int> &solution)
{
    int cost = 0;
    for (int i = 0; i < dimension_; ++i)
        for (int k : adjacencies_[i])
            cost += flow_[solution[i]][solution[k]];

    return cost/2;
}

// Search in the Tabu Moves if the move r,s is allowed with the vector current solution
bool TabuSearch::checkMove(int r, int s, vector<int> &currentSolution)
{
    for (int n = 0; n < tabuList_.size(); ++n)
    {
        /*
        if ((tabuList_[n].i == r && tabuList_[n].j == s ))
        {
            return false;
        }

        if ((tabuList_[n].i == s && tabuList_[n].j == r ))
        {
            return false;
        }*/

        
        if ((tabuList_[n].i == r && tabuList_[n].posI == currentSolution[r] ))
        {
            return false;
        }

        if ((tabuList_[n].i == s && tabuList_[n].posI == currentSolution[s] ))
        {
            return false;
        }
      
        if ((tabuList_[n].j == r && tabuList_[n].posJ == currentSolution[r] ))
        {
            return false;
        }

        if ((tabuList_[n].j == s && tabuList_[n].posJ == currentSolution[s] ))
        {
            return false;
        }
    }

    return true;
}

vector<int> TabuSearch::getSolution()
{
    return solution_;
}

int TabuSearch::getCost()
{
    return cost_;
}


