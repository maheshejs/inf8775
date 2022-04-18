#include "tabuSearch.h"
#include <algorithm>
#include <random>
#include <cmath>
#include <fstream>


TabuSearch::TabuSearch(const Input &input, int neighbourhoodSize, int maxFails)
    : dimension_(input.getDimension()), flow_(input.getFlow()), adjacency_(input.getAdjacency()), frequencies_(input.getFrequencies())
{
  solution_.resize(dimension_);

  // Fix parameters
  neighbourhoodSize_ = neighbourhoodSize;
  maxFails_ = maxFails;

  execute();
}

void TabuSearch::execute()
{

  // Randdom
  default_random_engine gen;
  uniform_int_distribution<> dist_int(0, dimension_ - 1);
  uniform_real_distribution<double> dist_real(0.0, 1.0);

  // Inner parameters
  int tabuLength = dimension_ > 750 ? dimension_/10 : dimension_/20 ;
  int fails = 0;
  bool improvement = false;

  // Initialize
  for (int i = 0; i < dimension_; ++i)
    solution_[i] = i;

  // Shuffle vector
  shuffle(solution_.begin(), solution_.end(), gen);

  // Get cost
  cost_ = calculateCost(solution_);

  // Current solution and cost
  vector<int> currentSolution = solution_;
  int currentCost = cost_;

  // cout << " Tabu search " << endl;
  bool isTabu = true;
  while (true)
  {
    if (isTabu)
    {
      improvement = false;

      // Empty the neighborhoud
      priority_queue<Neighbour, vector<Neighbour>, greater<Neighbour>> neighbourhood;

      // Generate the Neighbourhood
      for (int i = 0; i < neighbourhoodSize_; ++i)
      {
        // Generate random r and s
        int r = dist_int(gen);
        int s = dist_int(gen);

        // Add to the neighbourhood
        Neighbour neighbour;
        neighbour.r = r;
        neighbour.s = s;
        neighbour.cost = currentCost + moveCost(currentSolution, r, s);

        neighbourhood.push(neighbour);
      }

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
      while (!selected && !neighbourhood.empty())
      {
        best_neigh = neighbourhood.top();
        if (best_neigh.cost != currentCost)
          selected = checkMove(best_neigh.r, best_neigh.s, currentSolution);
        neighbourhood.pop();
      }

      // If none of the neighbourhood is selected, generate new neighbourhood
      if (!selected)
        continue;

      int r = best_neigh.r;
      int s = best_neigh.s;

      // Jump to something
      swap(currentSolution[r], currentSolution[s]);
      currentCost = best_neigh.cost;

      if (currentCost < cost_)
      {
        improvement = true;
        solution_ = currentSolution;
        cost_ = currentCost;
        cout << "\tCost: " << cost_ << endl;
        printSolution();
      }

      // Create tabu move
      TabuMove tabuMove;
      tabuMove.posI = currentSolution[r];
      tabuMove.posJ = currentSolution[s];
      tabuMove.i = r;
      tabuMove.j = s;

      // Add tabu move
      tabuList_.push_back(tabuMove);

      // Size of the deque
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
        fails++;
        if (fails == maxFails_)
        {
          fails = 0;
          isTabu = false;
          // cout << " Random improvement " << endl;
          currentSolution = solution_;
          currentCost = cost_;
        }
      }
    }
    else
    {
      int r = dist_int(gen);
      int s = dist_int(gen);

      currentCost = cost_ + moveCost(currentSolution, r, s);
      if (currentCost <= cost_)
      {
        swap(currentSolution[r], currentSolution[s]);
        solution_ = currentSolution;
        if (currentCost < cost_)
        {
          cout << "\tCost: " << currentCost << endl;
          printSolution();
        }
        cost_ = currentCost;
      }
    }
  }
}

int TabuSearch::moveCost(vector<int> &oldSolution, int r, int s)
{
  int cost = 0;
  for (int k : adjacency_[r])
    if (k != s)
      cost += flow_[oldSolution[s]][oldSolution[k]] - flow_[oldSolution[r]][oldSolution[k]];

  for (int k : adjacency_[s])
    if (k != r)
      cost += flow_[oldSolution[r]][oldSolution[k]] - flow_[oldSolution[s]][oldSolution[k]];

  return cost;
}

int TabuSearch::calculateCost(vector<int> &solution)
{
  int cost = 0;
  for (int i = 0; i < dimension_; ++i)
    for (int k : adjacency_[i])
      cost += flow_[solution[i]][solution[k]];

  return cost >> 1;
}

// Search in the Tabu Moves if the move r,s is allowed with the vector current solution
bool TabuSearch::checkMove(int r, int s, vector<int> &currentSolution)
{
  for (int n = 0; n < tabuList_.size(); ++n)
  {
    if ((tabuList_[n].i == r && tabuList_[n].posI == currentSolution[r]))
    {
      return false;
    }

    if ((tabuList_[n].i == s && tabuList_[n].posI == currentSolution[s]))
    {
      return false;
    }

    if ((tabuList_[n].j == r && tabuList_[n].posJ == currentSolution[r]))
    {
      return false;
    }

    if ((tabuList_[n].j == s && tabuList_[n].posJ == currentSolution[s]))
    {
      return false;
    }
  }

  return true;
}

void TabuSearch::printSolution()
{
  ofstream data_w("soln");
  for (int i = 0; i < dimension_; ++i)
  {
    int r = 0;
    int elem = solution_[i];
    while (elem >= frequencies_[r++]);
    cout << r-1 << " ";
    data_w << r-1 << " ";
  }
  cout << endl;
  data_w.close();
}
